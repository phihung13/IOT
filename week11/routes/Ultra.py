from fastapi import APIRouter, Depends
from models.user_model import *
from schemas.schema import ultra_serializer, ultras_serializer
from config.db import *
from datetime import datetime
from auth import auth
from emqx.pub import pub_ultra
from emqx.pub import pub_all

# ultra = APIRouter(dependencies=[Depends(auth.validate_api_key)])
ultra = APIRouter()

# POST method to send ultra to server
@ultra.post("/api/ultra/")
async def post_create_ultra(ultra: Ultra):
    ultra = dict(ultra)
    pub_all(device_name= ultra["device_name"], data={"ultra": ultra["ultra"]})
    result = pub_ultra(device_name= ultra["device_name"], ultra=ultra["ultra"])
    return {"status": "Ok","data": result}

# GET method to send ultra to server
@ultra.get("/api/ultra/")
async def get_create_ultra(device_name: str, ultra: int ):  
    pub_all(device_name= device_name, data={"ultra": ultra})
    result = pub_ultra(device_name= device_name, ultra= ultra)
    return {"status": "Ok","data": result}


@ultra.get("/api/get_all_ultra")
async def find_all_records():
    records = ultras_serializer(collection_ultra.find({}).sort([['_id', -1]] ))
    return records

# EMQX Broker post ultra to API server
@ultra.post("/api/emqx/ultra/")
async def broker_post_ultra(ultra: Ultra):
    ultra = dict(ultra)
    ultra["time"] = datetime.now()
    _id = collection_ultra.insert_one(ultra)
    ultra = ultras_serializer(collection_ultra.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": ultra}