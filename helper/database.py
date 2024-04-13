import pymongo
import os
from typing import Tuple, Union

from helper.date import add_date

# Retrieve MongoDB configuration from environment variables
DB_NAME = os.environ.get("DB_NAME", "")
DB_URL = os.environ.get("DB_URL", "")
mongo = pymongo.MongoClient(DB_URL)
db = mongo[DB_NAME]
dbcol = db["user"]

def total_user() -> int:
    """Returns the total number of users in the database."""
    return dbcol.count_documents({})

def botdata(chat_id: int) -> None:
    """Inserts bot data for a chat_id if it doesn't exist."""
    bot_data = {"_id": chat_id, "total_rename": 0, "total_size": 0}
    try:
        dbcol.insert_one(bot_data)
    except pymongo.errors.DuplicateKeyError:
        # Bot data already exists for this chat_id
        pass

def total_rename(chat_id: int, renamed_file: int) -> None:
    """Increments the total number of renamed files by one."""
    new_rename_count = renamed_file + 1
    dbcol.update_one({"_id": chat_id}, {"$set": {"total_rename": new_rename_count}})

def total_size(chat_id: int, current_total_size: int, new_file_size: int) -> None:
    """Updates the total size of files for a user."""
    new_total_size = current_total_size + new_file_size
    dbcol.update_one({"_id": chat_id}, {"$set": {"total_size": new_total_size}})

def insert(chat_id: int) -> bool:
    """Inserts a new user with default values."""
    user_data = {
        "_id": chat_id,
        "file_id": None,
        "caption": None,
        "daily": 0,
        "date": 0,
        "uploadlimit": 2147483648,  # 2GB limit
        "used_limit": 0,
        "usertype": "Free",
        "prexdate": None,
    }
    try:
        dbcol.insert_one(user_data)
        return True
    except pymongo.errors.DuplicateKeyError:
        # User already exists
        return False

def addthumb(chat_id: int, file_id: str) -> None:
    """Updates the thumbnail file ID for a user."""
    dbcol.update_one({"_id": chat_id}, {"$set": {"file_id": file_id}})

def delthumb(chat_id: int) -> None:
    """Deletes the thumbnail file ID for a user."""
    dbcol.update_one({"_id": chat_id}, {"$set": {"file_id": None}})

def addcaption(chat_id: int, caption: str) -> None:
    """Updates the caption for a user."""
    dbcol.update_one({"_id": chat_id}, {"$set": {"caption": caption}})

def delcaption(chat_id: int) -> None:
    """Deletes the caption for a user."""
    dbcol.update_one({"_id": chat_id}, {"$set": {"caption": None}})

def dateupdate(chat_id: int, date: int) -> None:
    """Updates the date for a user."""
    dbcol.update_one({"_id": chat_id}, {"$set": {"date": date}})

def used_limit(chat_id: int, used: int) -> None:
    """Updates the used limit for a user."""
    dbcol.update_one({"_id": chat_id}, {"$set": {"used_limit": used}})

def usertype(chat_id: int, user_type: str) -> None:
    """Updates the user type for a user."""
    dbcol.update_one({"_id": chat_id}, {"$set": {"usertype": user_type}})

def uploadlimit(chat_id: int, limit: int) -> None:
    """Updates the upload limit for a user."""
    dbcol.update_one({"_id": chat_id}, {"$set": {"uploadlimit": limit}})

def backpre(chat_id: int) -> None:
    """Resets the premium expiration date for a user."""
    dbcol.update_one({"_id": chat_id}, {"$set": {"prexdate": None}})

def addpre(chat_id: int) -> None:
    """Adds a premium expiration date for a user."""
    expiration_date = add_date()
    dbcol.update_one({"_id": chat_id}, {"$set": {"prexdate": expiration_date[0]}})

def addpredata(chat_id: int) -> None:
    """Resets premium data for a user."""
    dbcol.update_one({"_id": chat_id}, {"$set": {"prexdate": None}})

def daily(chat_id: int, date: int) -> None:
    """Updates the daily date for a user."""
    dbcol.update_one({"_id": chat_id}, {"$set": {"daily": date}})

def find(chat_id: int) -> Union[Tuple[str, Union[str, None]], None]:
    """Finds a user and returns the file ID and caption."""
    user = dbcol.find_one({"_id": chat_id})
    if user:
        return user.get("file_id"), user.get("caption")
    return None

def getid() -> list:
    """Returns a list of all user IDs."""
    return [key["_id"] for key in dbcol.find()]

def delete(chat_id: int) -> None:
    """Deletes a user by their chat ID."""
    dbcol.delete_one({"_id": chat_id})

def find_one(chat_id: int):
    """Finds one user by their chat ID."""
    return dbcol.find_one({"_id": chat_id})
	
