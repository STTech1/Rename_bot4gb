from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    # Check if the reply message contains a ForceReply markup
    if (message.reply_to_message.reply_markup and
        isinstance(message.reply_to_message.reply_markup, ForceReply)):
        
        new_name = message.text
        await message.delete()

        # Get the media message being replied to
        media = await client.get_messages(message.chat.id, message.reply_to_message.id)
        file = media.reply_to_message.document or media.reply_to_message.video or media.reply_to_message.audio
        
        if file:
            filename = file.file_name
            mime = file.mime_type.split("/")[0]
            mg_id = media.reply_to_message.id
            
            try:
                # Split the new filename and check for extension
                out = new_name.split(".")
                out_filename = new_name
                file_extension = out[-1]
                
                # Delete the original message with the ForceReply markup
                await message.reply_to_message.delete()

                # Create inline keyboard markup based on MIME type
                if mime == "video":
                    markup = InlineKeyboardMarkup([
                        [InlineKeyboardButton("📁 Document", callback_data="doc"),
                         InlineKeyboardButton("🎥 Video", callback_data="vid")]
                    ])
                elif mime == "audio":
                    markup = InlineKeyboardMarkup([
                        [InlineKeyboardButton("📁 Document", callback_data="doc"),
                         InlineKeyboardButton("🎵 Audio", callback_data="aud")]
                    ])
                else:
                    markup = InlineKeyboardMarkup([
                        [InlineKeyboardButton("📁 Document", callback_data="doc")]
                    ])

                # Reply with output file options and filename
                await message.reply_text(
                    f"**Select the output file type**\n**Output Filename** :- ```{out_filename}```",
                    reply_to_message_id=mg_id,
                    reply_markup=markup
                )

            except IndexError:
                # If there is an issue with the file extension, handle it
                logger.error(f"Invalid file extension in filename: {new_name}")
                await message.reply_to_message.delete()
                await message.reply_text(
                    "**Error**: Invalid filename or missing extension. Please provide a valid filename.",
                    reply_to_message_id=mg_id
                )
        else:
            logger.warning(f"No document, video, or audio found in the reply message from user {message.from_user.id}")
            await message.reply_text(
                "**Error**: No media file found in the replied message.",
                reply_to_message_id=mg_id
            )
                
