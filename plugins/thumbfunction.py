from pyrogram import Client, filters
from helper.database import find, delthumb, addthumb
from pyrogram.types import Message

@Client.on_message(filters.private & filters.command(['viewthumb']))
async def viewthumb(client: Client, message: Message):
    """
    Send the user's custom thumbnail to the user if it exists.
    """
    chat_id = message.chat.id
    thumb_data = find(chat_id)
    
    # Check if user has a custom thumbnail
    if thumb_data and len(thumb_data) > 0:
        thumb = thumb_data[0]
        await client.send_photo(chat_id, photo=thumb)
    else:
        await message.reply_text("**You don't have any custom thumbnail.**")

@Client.on_message(filters.private & filters.command(['delthumb']))
async def removethumb(client: Client, message: Message):
    """
    Delete the user's custom thumbnail if it exists.
    """
    chat_id = message.chat.id
    delthumb(chat_id)
    await message.reply_text("**Custom thumbnail deleted successfully.**")

@Client.on_message(filters.private & filters.photo)
async def addthumbs(client: Client, message: Message):
    """
    Save the user's custom thumbnail.
    """
    chat_id = message.chat.id
    
    # Check if the photo is available
    if message.photo:
        file_id = str(message.photo.file_id)
        addthumb(chat_id, file_id)
        await message.reply_text("**Custom thumbnail saved successfully.** ✅")
    else:
        await message.reply_text("**Failed to save custom thumbnail. Please try again.**")

