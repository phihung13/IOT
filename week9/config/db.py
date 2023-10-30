from pymongo import MongoClient

MONGO_INITDB_ROOT_USERNAME="reone"
MONGO_INITDB_ROOT_PASSWORD="50fyIuZCO23UBLXV"
MONGO_INITDB_DATABASE="REONE"

DATABASE_URL=f"mongodb+srv://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@reone.noidfzq.mongodb.net/?retryWrites=true&w=majority"

db_connection = MongoClient(DATABASE_URL)
db = db_connection.database_name
collection = db["TH"]