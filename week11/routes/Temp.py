from fastapi import APIRouter, Depends
from models.user_model import *
from schemas.schema_temp import temp_serializer, temps_serializer
from config.db import *
from datetime import datetime
from auth import auth
from emqx.http_publish import pub_temp

# temp = APIRouter(dependencies=[Depends(auth.validate_api_key)])
temp = APIRouter()

# POST method to send TEMP to server
@temp.post("/api/temp/")
async def post_create_temp(temp: Temp):
    temp = dict(temp)
    result = pub_temp(device_name= temp["device_name"], temp=temp["temp"])
    return {"status": "Ok","data": result}

# GET method to send TEMP to server
@temp.get("/api/temp/{temp}")
async def get_create_temp(device_name: str, temp: int ):  
    result = pub_temp(device_name= device_name, temp= temp)
    return {"status": "Ok","data": result}

@temp.get("/api/get_all_temp")
async def find_all_records():
    records = temps_serializer(collection_temp.find({}).sort([['_id', -1]] ))
    return records

# EMQX Broker post TEMP to API server
@temp.post("/api/emqx/temp/")
async def broker_post_temp(temp: Temp):
    temp = dict(temp)
    temp["time"] = datetime.now()
    _id = collection_temp.insert_one(temp)
    temp = temps_serializer(collection_temp.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": temp}