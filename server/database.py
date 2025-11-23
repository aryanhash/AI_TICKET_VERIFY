from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
DATABASE_NAME = "nft_ticketing"

client = MongoClient(MONGO_URL)
db = client[DATABASE_NAME]

users_collection = db["users"]
events_collection = db["events"]
tickets_collection = db["tickets"]
verifications_collection = db["verifications"]

def get_database():
    return db
