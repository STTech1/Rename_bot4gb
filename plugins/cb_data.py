from pyrogram import Client, filters
from pyrogram.types import ForceReply, Message
from helper.progress import progress_for_pyrogram
from helper.database import find_one, used_limit, dateupdate, find
from helper.ffmpeg import take_screen_shot, fix_thumb
from helper.set import escape_invalid_curly_brackets
from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import os
import time
from datetime import timedelta
from helper.progress import humanbytes
import logging
import requests  # For downloading files from URLs
from urllib.parse import urlparse

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
API_ID = int(os.getenv("API_ID", ""))
API_HASH = os.getenv("API_HASH", "")
STRING = os.getenv("STRING", "")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", ""))

app = Client("test", api_id=API_ID, api_hash=API_HASH, session_string=STRING)

# Helper functions
def calculate_used_limit(user_id, file_size, increase=True):
    user_data = find_one(user_id)
    used_limit = user_data.get("used_limit", 0)
    if increase:
        new_used_limit = used_limit + file_size
    else:
        new_used_limit = used_limit - file_size
    used_limit(user_id, new_used_limit)
    return new_used_limit

async def download_file(bot, file, message, ms):
    try:
        c_time = time.time()
        path = await bot.download_media(
            message=file,
            progress=progress_for_pyrogram,
            progress_args=("```Trying To Download...```", ms, c_time)
        )
        return path
    except Exception as e:
        await ms.edit(f"Error downloading file: {e}")
        return None

async def download_from_url(url, file_path):
    """Download a file from the given URL to the specified file path."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return file_path
    except requests.RequestException as e:
        logger.error(f"Error downloading from URL: {e}")
        return None

async def process_and_upload_file(bot, file_path, user_id, thumb, duration, c_caption, file_size, ms, file_type="doc"):
    await upload_file(bot, file_path, user_id, thumb, duration, c_caption, file_size, ms, file_type)

async def upload_file(bot, file_path, user_id, thumb, duration, c_caption, file_size, ms, file_type="doc"):
    c_time = time.time()
    caption = f"**{os.path.basename(file_path)}**"
    if c_caption:
        caption = c_caption.format(
            filename=os.path.basename(file_path),
            filesize=humanbytes(file_size),
            duration=timedelta(seconds=duration) if duration else ""
        )
    
    upload_func = {
        "doc": bot.send_document,
        "vid": bot.send_video,
        "aud": bot.send_audio
    }[file_type]

    try:
        await upload_func(
            user_id,
            document=file_path if file_type == "doc" else None,
            video=file_path if file_type == "vid" else None,
            audio=file_path if file_type == "aud" else None,
            thumb=thumb,
            duration=duration if file_type in ["vid", "aud"] else None,
            caption=caption,
            progress=progress_for_pyrogram,
            progress_args=("```Trying To Upload...```", ms, c_time)
        )
        await ms.delete()
        os.remove(file_path)
        if thumb:
            os.remove(thumb)
    except Exception as e:
        calculate_used_limit(user_id, file_size, increase=False)
        await ms.edit(f"Error uploading file: {e}")
        os.remove(file_path)
        if thumb:
            os.remove(thumb)

# Event handlers
@app.on_callback_query(filters.regex('cancel'))
async def cancel(bot, update):
    try:
        await update.message.delete()
    except Exception as e:
        logger.error(f"Error in cancel handler: {e}")

@app.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    chat_id = update.message.chat.id
    date_fa = str(update.message.date)
    pattern = '%Y-%m-%d %H:%M:%S'
    date = int(time.mktime(time.strptime(date_fa, pattern)))
    await update.message.delete()
    await update.message.reply_text(
        f"__Please enter the new filename...__\n\nNote:- Extension Not Required",
        reply_to_message_id=update.message.reply_to_message_id,
        reply_markup=ForceReply(True)
    )
    dateupdate(chat_id, date)

@app.on_message(filters.text & filters.regex(r'http[s]?://') & filters.private)
async def handle_url(bot: Client, message: Message):
    user_id = message.from_user.id
    url = message.text.strip()
    
    # Validate URL
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        await message.reply_text("Invalid URL.")
        return

    # Extract filename from the URL
    filename = os.path.basename(parsed_url.path)
    file_extension = os.path.splitext(filename)[1]
    
    # Define file path
    file_path = f"downloads/{filename}"

    # Replying with a progress message
    ms = await message.reply_text("```Downloading file from URL...```")
    
    # Download file from URL
    downloaded_file_path = await download_from_url(url, file_path)
    if not downloaded_file_path:
        await ms.edit("Failed to download the file from the URL.")
        return

    # Process and upload the file
    await process_and_upload_file(bot, downloaded_file_path, user_id, None, 0, None, os.path.getsize(downloaded_file_path), ms)

app.run()
	
