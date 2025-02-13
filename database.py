from pymongo import MongoClient
from config import DATABASE_URL, DB_NAME

client = MongoClient(DATABASE_URL)
db = client[DB_NAME]
