from datetime import datetime, timedelta
from pymongo import MongoClient
from config import DB_URI, DB_NAME, FILE_EXPIRATION_TIME, MAX_FILE_DOWNLOADS



import pymongo, os
from config import DB_URI, DB_NAME


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]


user_data = database['users']

async def add_file_with_expiry(file_id, expiration_time=FILE_EXPIRATION_TIME):
    expiry = datetime.utcnow() + timedelta(seconds=expiration_time)
    file_data.update_one(
        {'_id': file_id},
        {'$set': {'expiry_time': expiry}},
        upsert=True
    )

async def get_expired_files():
    current_time = datetime.utcnow()
    return list(file_data.find({
        'expiry_time': {'$lt': current_time}
    }))

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
