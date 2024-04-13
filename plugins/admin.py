import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from helper.database import uploadlimit, usertype, addpre
from helper.date import add_date

# Define admin user ID from the environment
ADMIN = int(os.environ.get("ADMIN", 5076254266))

# Define premium plans in a dictionary for dynamic configuration
PREMIUM_PLANS = {
    "vip1": {
        "name": "VIP 1",
        "limit": 10 * 1024**3,  # 10 GB
        "description": "Hey, you have been upgraded to VIP 1. Check your plan with /myplan."
    },
    "vip2": {
        "name": "VIP 2",
        "limit": 50 * 1024**3,  # 50 GB
        "description": "Hey, you have been upgraded to VIP 2. Check your plan with /myplan."
    }
}

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["warn"]))
async def warn(client, message):
    if len(message.command) < 3:
        await message.reply_text("Usage: /warn <user_id> <reason>")
        return
    
    user_id = message.command[1]
    reason = ' '.join(message.command[2:])
    
    try:
        await client.send_message(chat_id=int(user_id), text=reason)
        await message.reply_text("User notified successfully.")
    except Exception as e:
        await message.reply_text(f"Failed to notify user. Error: {e}")

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["addpremium"]))
async def add_premium_plan(client, message):
    # Offer choices for premium plans
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("VIP 1", callback_data="vip1")],
        [InlineKeyboardButton("VIP 2", callback_data="vip2")]
    ])
    await message.reply_text("Select a plan:", reply_markup=keyboard)

@Client.on_callback_query(filters.regex("vip1|vip2"))
async def handle_premium_selection(client, query):
    plan_id = query.data
    user_id = query.message.reply_to_message.text.split()[1]
    
    # Get the selected plan details
    plan = PREMIUM_PLANS.get(plan_id)
    if not plan:
        await query.message.edit_text("Invalid selection. Please try again.")
        return
    
    # Update user's plan and upload limit
    uploadlimit(int(user_id), plan["limit"])
    usertype(int(user_id), plan["name"])
    addpre(int(user_id))
    
    # Provide feedback
    await query.message.edit_text(f"Added {plan['name']} successfully. Upload limit: {plan['limit'] // (1024**3)} GB")
    await client.send_message(int(user_id), plan["description"])

