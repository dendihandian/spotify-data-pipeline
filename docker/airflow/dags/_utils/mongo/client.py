from _configs.mongo import MONGO_CONFIG
from pymongo import MongoClient

MONGO_HOST=MONGO_CONFIG['host']
MONGO_PORT=MONGO_CONFIG['port']
MONGO_USER=MONGO_CONFIG['user']
MONGO_PASS=MONGO_CONFIG['pass']

mongo = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/")