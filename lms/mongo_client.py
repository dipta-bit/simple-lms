import os
from pymongo import MongoClient

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://mongodb:27017/lms_logs')
client = MongoClient(MONGO_URI)

db = client['lms_logs'] 

activity_logs = db['activity_logs']
learning_analytics = db['learning_analytics']