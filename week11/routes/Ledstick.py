from fastapi import APIRouter, Depends
from models.user_model import *
from schemas.schema_ledstick import ledstick_serializer, ledsticks_serializer
from config.db import *
from datetime import datetime
from auth import auth
from emqx.http_publish import pub_ledstick

# ledstick = APIRouter(dependencies=[Depends(auth.validate_api_key)])
ledstick = APIRouter()

# POST method to send ledstick to server
@ledstick.post("/api/ledstick/")
async def post_create_ledstick(ledstick: Ledstick):
    ledstick = dict(ledstick)
    result = pub_ledstick(device_name= ledstick["device_name"], ledstick=ledstick["ledstick"])
    return {"status": "Ok","data": result}

# GET method to send ledstick to server
@ledstick.get("/api/ledstick/")
async def get_create_ledstick(device_name: str, ledstick: int ): 
    result = pub_ledstick(device_name= device_name, ledstick= ledstick)
    return {"status": "Ok","data": result}


@ledstick.get("/api/get_all_ledstick")
async def find_all_records():
    records = ledsticks_serializer(collection_ledstick.find({}).sort([['_id', -1]] ))
    return records

# EMQX Broker post ledstick to API server
@ledstick.post("/api/emqx/ledstick/")
async def broker_post_ledstick(ledstick: Ledstick):
    ledstick = dict(ledstick)
    ledstick["time"] = datetime.now()
    _id = collection_ledstick.insert_one(ledstick)
    ledstick = ledsticks_serializer(collection_ledstick.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": ledstick}
