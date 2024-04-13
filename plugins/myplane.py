import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from datetime import datetime, date as date_
from helper.database import find_one, used_limit, daily as update_daily, uploadlimit, usertype, backpre
from helper.progress import humanbytes
from helper.date import check_expi

@Client.on_message(filters.private & filters.command(["myplan"]))
async def show_plan(client, message):
    user_id = message.from_user.id

    # Retrieve user data from the database
    user_data = find_one(user_id)
    daily_limit = user_data["daily"]
    today_timestamp = int(time.mktime(time.strptime(str(date_.today()), '%Y-%m-%d')))

    # Check if the user's daily limit needs to be updated
    if daily_limit != today_timestamp:
        update_daily(user_id, today_timestamp)
        used_limit(user_id, 0)
    
    # Get updated user data
    updated_user_data = find_one(user_id)
    used = updated_user_data["used_limit"]
    limit = updated_user_data["uploadlimit"]
    remain = limit - used
    user_type = updated_user_data["usertype"]
    plan_ends = updated_user_data.get("prexdate")

    # Handle plan expiration
    if plan_ends:
        if not check_expi(plan_ends):
            backpre(user_id)

    # Format the plan details for the message
    plan_details = (
        f"User ID: ```{user_id}```\n"
        f"Plan: {user_type}\n"
        f"Daily Upload Limit: {humanbytes(limit)}\n"
        f"Today Used: {humanbytes(used)}\n"
        f"Remain: {humanbytes(remain)}"
    )

    # Add plan end date if available
    if plan_ends:
        normal_date = datetime.fromtimestamp(plan_ends).strftime('%Y-%m-%d')
        plan_details += f"\nYour Plan Ends On: {normal_date}"
    
    # Determine reply markup based on user type
    if user_type == "Free":
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Upgrade 💰💳", callback_data="upgrade"),
             InlineKeyboardButton("Cancel ✖️", callback_data="cancel")]
        ])
    else:
        reply_markup = None

    # Send the plan details message to the user
    await message.reply(plan_details, quote=True, reply_markup=reply_markup)
	
