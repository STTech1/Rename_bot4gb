import os
from pyrogram import Client, filters
from helper.database import botdata, find_one, total_user
from helper.progress import humanbytes

# Load token from environment variable
token = os.environ.get('TOKEN', '')
bot_id = int(token.split(':')[0])

# Pyrogram client initialization
client = Client("my_bot", bot_token=token)


@client.on_message(filters.private & filters.command(["about"]))
async def about(client, message):
    try:
        # Initialize bot data
        botdata(bot_id)
        
        # Retrieve bot data
        data = find_one(bot_id)
        
        if data:
            total_rename = data.get("total_rename", 0)
            total_size = data.get("total_size", 0)
            
            # Create the response message
            response_message = (
                f"Total User: {total_user()}\n"
                f"Bot: @strenamer\n"
                f"Creator: @stthamizhan\n"
                f"Language: Python 3\n"
                f"Library: Pyrogram 2.0\n"
                f"Server: vps\n"
                f"Total Renamed Files: {total_rename}\n"
                f"Total Size Renamed: {humanbytes(total_size)}"
            )
            
            # Send the response message
            await message.reply_text(response_message, quote=True)
        else:
            await message.reply_text("Error: Could not retrieve bot data.", quote=True)
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}", quote=True)


if __name__ == "__main__":
    # Start the Pyrogram client
    client.run()
