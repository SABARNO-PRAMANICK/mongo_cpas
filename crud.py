import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional, Dict
from pymongo.errors import ConnectionFailure, OperationFailure
from pprint import pprint


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")


# print("Connecting to MongoDB...")
# client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
# client.admin.command('ping')
# print("Connection to MongoDB successful!")
# print("Databases:", client.list_database_names())
    


try:
    print("Connecting to MongoDB...")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    pprint(client.server_info())
    logger.info("Connection to MongoDB successful!")
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    collection.create_index("request_id", unique=True)
except ConnectionFailure as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise RuntimeError("Database connection failed")
except OperationFailure as e:
    logger.error(f"Database operation failed: {e}")
    raise RuntimeError("Database setup failed")


def input_helper(input_doc: dict) -> dict:
    return {
        "request_id": input_doc["request_id"],
        "input": input_doc["input"],
        "metadata": input_doc.get("metadata"),
        "date_time": input_doc["date_time"],
        "_id": str(input_doc["_id"]),
    }

def create_user_input(data: dict) -> dict:
    result = collection.insert_one(data)
    created_input = collection.find_one({"_id": result.inserted_id})
    return input_helper(created_input)

def get_all_user_inputs() -> List[dict]:
    return [input_helper(doc) for doc in collection.find()]

def get_user_input_by_id(request_id: str) -> Optional[dict]:
    doc = collection.find_one({"request_id": request_id})
    if doc:
        return input_helper(doc)
    return None

def replace_user_input(request_id: str, data: dict) -> Optional[dict]:
    result = collection.replace_one({"request_id": request_id}, data)
    if result.matched_count == 1:
        updated_input = collection.find_one({"request_id": request_id})
        return input_helper(updated_input)
    return None

def partial_update_user_input(request_id: str, update_dict: dict) -> Optional[dict]:
    result = collection.update_one({"request_id": request_id}, {"$set": update_dict})
    if result.modified_count == 1:
        updated_input = collection.find_one({"request_id": request_id})
        return input_helper(updated_input)
    return None