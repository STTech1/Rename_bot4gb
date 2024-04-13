import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError
from helper.database import getid, delete
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Admin ID from environment variable
ADMIN = int(os.environ.get("ADMIN", 923943045))

# Function to send broadcast messages
@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["broadcast"]))
async def broadcast(bot, message):
    # Check if the command is a reply to a message
    if message.reply_to_message:
        # Retrieve user IDs from the database
        ms = await message.reply_text("Retrieving all user IDs from the database...")
        ids = getid()
        total_users = len(ids)
        
        # Initialize counters
        success_count = 0
        failed_count = 0
        
        # Update admin on the start of the broadcast
        await ms.edit_text(f"Starting broadcast... Sending message to {total_users} users.")
        
        # Iterate through each user ID and send the message
        for user_id in ids:
            try:
                # Send the message to the user
                await message.reply_to_message.copy(user_id)
                success_count += 1
                
                # Control the rate of message sending to avoid FloodWait
                await asyncio.sleep(0.5)
                
            except FloodWait as e:
                # Handle FloodWait by sleeping for the specified duration
                logger.info(f"FloodWait: Sleeping for {e.x} seconds.")
                await asyncio.sleep(e.x)
            
            except RPCError as e:
                # Log and handle other RPC errors
                logger.error(f"RPCError: {e}")
                delete({"_id": user_id})
                failed_count += 1
            
            except Exception as e:
                # Handle any other exceptions
                logger.error(f"Unexpected error: {e}")
                failed_count += 1
        
        # Send a summary of the broadcast results to the admin
        summary_message = f"Broadcast completed.\n\n"
        summary_message += f"Messages sent successfully: {success_count}\n"
        summary_message += f"Messages failed: {failed_count}\n"
        summary_message += f"Total users targeted: {total_users}"
        await ms.edit_text(summary_message)

# You may add additional enhancements or functions as needed for your use case
