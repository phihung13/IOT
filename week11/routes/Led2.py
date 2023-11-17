from fastapi import APIRouter, Depends
from models.user_model import *
from schemas.schema import led2_serializer, led2s_serializer
from config.db import *
from datetime import datetime
from auth import auth
from emqx.pub import pub_led2
from emqx.pub import pub_all

# led2 = APIRouter(dependencies=[Depends(auth.validate_api_key)])
led2 = APIRouter()


# POST method to send led2 to server
@led2.post("/api/led2/")
async def post_create_led2(led2: Led2):
    led2 = dict(led2)
    pub_all(device_name= led2["device_name"], data={"led2": led2["led2"]})
    result = pub_led2(device_name= led2["device_name"], led2=led2["led2"])
    return {"status": "Ok","data": result}

# GET method to send led2 to server
@led2.get("/api/led2/")
async def get_create_led2(device_name: str, led2: bool ):
    pub_all(device_name= device_name, data={"led2": led2})   
    result = pub_led2(device_name= device_name, led2=led2)
    return {"status": "Ok","data": result}

@led2.get("/api/get_all_led2")
async def find_all_records():
    records = led2s_serializer(collection_led2.find({}).sort([['_id', -1]] ))
    return records

# EMQX Broker post led2 to API server
@led2.post("/api/emqx/led2/")
async def broker_post_led2(led2: Led2):
    led2 = dict(led2)
    led2["time"] = datetime.now()
    _id = collection_led2.insert_one(led2)
    led2 = led2s_serializer(collection_led2.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": led2}