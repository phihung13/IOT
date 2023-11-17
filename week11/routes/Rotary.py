from fastapi import APIRouter, Depends
from models.user_model import *
from schemas.schema import rotary_serializer, rotarys_serializer
from config.db import *
from datetime import datetime
from auth import auth
from emqx.pub import pub_rotary
from emqx.pub import pub_all

# rotary = APIRouter(dependencies=[Depends(auth.validate_api_key)])
rotary = APIRouter()

# POST method to send rotary to server
@rotary.post("/api/rotary/")
async def post_create_rotary(rotary: Rotary):
    rotary = dict(rotary)
    pub_all(device_name= rotary["device_name"], data={"rotary": rotary["rotary"]})
    result = pub_rotary(device_name= rotary["device_name"], rotary=rotary["rotary"])
    return {"status": "Ok","data": result}

# GET method to send rotary to server
@rotary.get("/api/rotary/")
async def get_create_rotary(device_name: str, rotary: int ):  
    pub_all(device_name= device_name, data={"rotary": rotary})
    result = pub_rotary(device_name= device_name, rotary= rotary)
    return {"status": "Ok","data": result}


@rotary.get("/api/get_all_rotary")
async def find_all_records():
    records = rotarys_serializer(collection_rotary.find({}).sort([['_id', -1]] ))
    return records

# EMQX Broker post rotary to API server
@rotary.post("/api/emqx/rotary/")
async def broker_post_rotary(rotary: Rotary):
    rotary = dict(rotary)
    rotary["time"] = datetime.now()
    _id = collection_rotary.insert_one(rotary)
    rotary = rotarys_serializer(collection_rotary.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": rotary}