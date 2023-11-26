from fastapi import APIRouter, Depends
from models.user_model import *
from schemas.schema_light import light_serializer, lights_serializer
from config.db import *
from datetime import datetime
from auth import auth
from emqx.http_publish import pub_light

# light = APIRouter(dependencies=[Depends(auth.validate_api_key)])
light = APIRouter()

# POST method to send light to server
@light.post("/api/light/")
async def post_create_light(light: Light):
    light = dict(light)
    result = pub_light(device_name= light["device_name"], light=light["light"])
    return {"status": "Ok","data": result}

# GET method to send light to server
@light.get("/api/light/")
async def get_create_light(device_name: str, light: int ):  
    result = pub_light(device_name= device_name, light= light)
    return {"status": "Ok","data": result}


@light.get("/api/get_all_light")
async def find_all_records():
    records = lights_serializer(collection_light.find({}).sort([['_id', -1]] ))
    return records

# EMQX Broker post light to API server
@light.post("/api/emqx/light/")
async def broker_post_light(light: Light):
    light = dict(light)
    light["time"] = datetime.now()
    _id = collection_light.insert_one(light)
    light = lights_serializer(collection_light.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": light}