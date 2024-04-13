from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helper.database import find, addcaption, delcaption

# Define command handlers

@Client.on_message(filters.private & filters.command("set_caption"))
async def set_caption(client, message):
    """
    Handler for setting a custom caption for files.
    
    Command format: /set_caption [caption]
    """
    # Check if the command includes a caption
    if len(message.command) == 1:
        return await message.reply_text("**Please provide a caption to set.\n\nExample: `/set_caption File Name`**")
    
    # Extract the caption from the command
    caption = message.text.split(" ", 1)[1]
    
    # Set the caption in the database
    addcaption(int(message.chat.id), caption)
    
    # Respond with a success message
    await message.reply_text("**Your caption has been successfully added ✅**")

@Client.on_message(filters.private & filters.command("del_caption"))
async def delete_caption(client, message):
    """
    Handler for deleting a custom caption.
    
    Command format: /del_caption
    """
    # Find the user's current caption
    user_id = int(message.chat.id)
    _, caption = find(user_id)
    
    # Check if the user has a custom caption
    if not caption:
        return await message.reply_text("**You don't have any custom caption set.**")
    
    # Delete the caption from the database
    delcaption(user_id)
    
    # Respond with a success message
    await message.reply_text("**Your caption has been successfully deleted ✅**")

@Client.on_message(filters.private & filters.command("see_caption"))
async def see_caption(client, message):
    """
    Handler for viewing the current custom caption.
    
    Command format: /see_caption
    """
    # Find the user's current caption
    user_id = int(message.chat.id)
    _, caption = find(user_id)
    
    # Check if the user has a custom caption
    if caption:
        # Respond with the user's custom caption
        await message.reply_text(f"**Your Caption:**\n\n`{caption}`")
    else:
        # Respond if the user doesn't have a custom caption
        await message.reply_text("**You don't have any custom caption set.**")
