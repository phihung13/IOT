from fastapi import APIRouter, Depends
from models.user_model import *
from schemas import schema as scm
from config.db import *
from datetime import datetime
from auth import auth
from emqx.http_publish import pub_all

from typing import Dict, Any

# record = APIRouter(dependencies=[Depends(auth.validate_api_key)])
record = APIRouter()


# POST method to send data to server
@record.post("/api/all/")
async def post_create_record(record: Dict[str, Any]):
    record = dict(record)
    result = pub_all(device_name= record["device_name"], data=record["data"])
    return {"status": "Ok","data": result}

# GET method to send data to server
@record.get("/api/all/{record}/")
async def get_create_record(device_name: str, data: dict):  
    result = pub_all(device_name= device_name, data=data)
    return {"status": "Ok","data": result}

# EMQX Broker post data to API server
@record.post("/api/emqx/all/")
async def post_create_record(record: Dict[str, Any]):
    print(record)
    record = dict(record)
    record["time"] = datetime.now()
    _id = collection.insert_one(dict(record))
    record = scm.all_records(collection.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": record}


# get all record from server
@record.get("/api/getAll/")
async def find_all_records():
    records = scm.all_records(collection.find({}).sort([['_id', -1]] ))
    return {"status": "Ok","data": records}

# get the last n records from server
@record.get("/api/getNLast/{n}")
async def get_last_record(number : int):
   number_record = scm.records_serializer(collection.find().sort([['_id', -1]]).limit(number))
   return {"status": "Ok","data": number_record}

# @record.get("/api/getTime/{time}")
# async def get_record_by_time(start: datetime, end: datetime):

#    number_record = records_serializer(collection.find(
#     {
#         "time": {
#             "$gte": start,
#             "$lt" : end
#         }
#     }
#    ))
#    return {"status": "Ok","data": number_record}
