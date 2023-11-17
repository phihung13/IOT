from fastapi import APIRouter, Depends
from models.user_model import *
from schemas.schema import led1_serializer, led1s_serializer
from config.db import *
from datetime import datetime
from auth import auth
from emqx.pub import pub_led1
from emqx.pub import pub_all

# led1 = APIRouter(dependencies=[Depends(auth.validate_api_key)])
led1 = APIRouter()


# POST method to send led1 to server
@led1.post("/api/led1/")
async def post_create_led1(led1: Led1):
    led1 = dict(led1)
    pub_all(device_name= led1["device_name"], data={"led1": led1["led1"]})
    result = pub_led1(device_name= led1["device_name"], led1=led1["led1"])
    return {"status": "Ok","data": result}

# GET method to send led1 to server
@led1.get("/api/led1/")
async def get_create_led1(device_name: str, led1: bool ):
    pub_all(device_name= device_name, data={"led1": led1})   
    result = pub_led1(device_name= device_name, led1=led1)
    return {"status": "Ok","data": result}

@led1.get("/api/get_all_led1")
async def find_all_records():
    records = led1s_serializer(collection_led1.find({}).sort([['_id', -1]] ))
    return records

# EMQX Broker post led1 to API server
@led1.post("/api/emqx/led1/")
async def broker_post_led1(led1: Led1):
    led1 = dict(led1)
    led1["time"] = datetime.now()
    _id = collection_led1.insert_one(led1)
    led1 = led1s_serializer(collection_led1.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": led1}
