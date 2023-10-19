from fastapi import APIRouter
from models.user_model import Record
from schemas.record_schema import records_serializer
from config.db import collection
from datetime import datetime
from fastapi import FastAPI, Body, Depends, HTTPException, status
from fastapi.responses import HTMLResponse

from auth import auth



# record = APIRouterR(dependencies=[Depends(auth.validate_api_key)])

record = APIRouter()

# Use POST method to send data to server
@record.post("/api")
async def post_create_record(record: Record):
    _id = collection.insert_one(dict(record))
    record = records_serializer(collection.find({"_id": _id.inserted_id}))
    print(record[0]["time"])
    return {"status": "Ok","data": record}


# get all record from server
@record.get("/api/getAll")
async def find_all_records():
    records = records_serializer(collection.find({}).sort([['_id', -1]] ))
    return {"status": "Ok","data": records}

# Use GET method to send data to server
@record.get("/api/{record}")
async def get_create_record(device_name: str, tem: int , humi: int , led1: bool, led2: bool, time: datetime = datetime.now() ):  
    record = {
        "device_name" : device_name,
        "time" : time,
        "tem" : tem,
        "humi" : humi,
        "led1" : led1,
        "led2" : led2,
   }
    _id = collection.insert_one(dict(record))
    record = records_serializer(collection.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": record}

# get one record by id  
# @record.get("/api/getOne/{id}")
# async def get_one_record(id: str):
#    record = records_serializer(collection.find({"_id": ObjectId(id)}))
#    return {"status": "Ok","data": record}

# get the last n records from server
@record.get("/api/getNLast/{n}")
async def get_last_record(number : int):
   number_record = records_serializer(collection.find().sort([['_id', -1]] ).limit(number))
   return {"status": "Ok","data": number_record}

# @record.get("/api/getNLast/{time}")
# async def get_record_by_time(start_time: datetime = datetime.now()  , end_time: datetime = datetime.now()):
#    number_record = records_serializer(collection.find({}))
#    return {"status": "Ok","data": number_record}

@record.get("/api/getTime/{time}")
async def get_record_by_time(start: datetime, end: datetime):
   number_record = records_serializer(collection.find(
    {
        "time": {
            "$gte": start,
            "$lt" : end
        }
    }
   ))
   return {"status": "Ok","data": number_record}

@record.get("/graph/", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
