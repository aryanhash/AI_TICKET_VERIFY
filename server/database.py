from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
DATABASE_NAME = "nft_ticketing"

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    # Test connection
    client.server_info()
    print(f"✓ MongoDB connected: {MONGO_URL}")
except Exception as e:
    print(f"✗ MongoDB connection failed: {e}")
    print("Please start MongoDB or check your MONGO_URL in .env")
    print("See MONGODB_SETUP.md for instructions")
    client = None

db = client[DATABASE_NAME] if client else None

users_collection = db["users"]
events_collection = db["events"]
tickets_collection = db["tickets"]
verifications_collection = db["verifications"]

def get_database():
    return db
