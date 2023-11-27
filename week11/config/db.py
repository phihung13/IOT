from pymongo import MongoClient

MONGO_INITDB_ROOT_USERNAME="reone"
MONGO_INITDB_ROOT_PASSWORD="50fyIuZCO23UBLXV"
MONGO_INITDB_DATABASE="REONE"

DATABASE_URL=f"mongodb+srv://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@reone.noidfzq.mongodb.net/?retryWrites=true&w=majority"

db_connection = MongoClient(DATABASE_URL)
db = db_connection.database_name

collection = db["ALL"]
collection_temp = db["TEMP"]
collection_humi = db["HUMI"]
collection_led1 = db["LED1"]
collection_led2 = db["LED2"]
collection_ledstick = db["LED Stick"]
collection_digit = db["DIGIT"]
collection_sonic = db["SONIC"]
collection_light = db["LIGHT"]
collection_lcd = db["LCD"]
collection_thump = db["THUMP"]