from datetime import datetime, timedelta
import pymongo
from config import DB_URI, DB_NAME, FILE_EXPIRATION_TIME

# Ensure database connection
try:
    dbclient = pymongo.MongoClient(DB_URI)
    database = dbclient[DB_NAME]
    
    # Create collections if they don't exist
    user_data = database['users']
    file_data = database['files']
except Exception as e:
    print(f"Database Connection Error: {e}")
    raise

async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

async def add_file_with_expiry(file_id, expiration_time=FILE_EXPIRATION_TIME):
    try:
        expiry = datetime.utcnow() + timedelta(seconds=expiration_time)
        file_data.update_one(
            {'_id': file_id},
            {'$set': {'expiry_time': expiry}},
            upsert=True
        )
    except Exception as e:
        print(f"Error adding file expiry: {e}")

async def get_expired_files():
    try:
        current_time = datetime.utcnow()
        return list(file_data.find({
            'expiry_time': {'$lt': current_time}
        }))
    except Exception as e:
        print(f"Error getting expired files: {e}")
        return []

async def remove_file_record(file_id):
    try:
        file_data.delete_one({'_id': file_id})
    except Exception as e:
        print(f"Error removing file record: {e}")
