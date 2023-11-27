from fastapi import APIRouter, Depends
from models.user_model import *
from schemas.schema_thump import thump_serializer, thumps_serializer
from config.db import *
from datetime import datetime
from auth import auth
from emqx.http_publish import pub_thump

# thump = APIRouter(dependencies=[Depends(auth.validate_api_key)])
thump = APIRouter()

# POST method to send thump to server
@thump.post("/api/thump/")
async def post_create_thump(thump: Thump):
    thump = dict(thump)
    result = pub_thump(device_name= thump["device_name"], thump=thump["thump"])
    return {"status": "Ok","data": result}

# GET method to send thump to server
@thump.get("/api/thump/")
async def get_create_thump(device_name: str, thump: int ): 
    result = pub_thump(device_name= device_name, thump= thump)
    return {"status": "Ok","data": result}


@thump.get("/api/get_all_thump")
async def find_all_records():
    records = thumps_serializer(collection_thump.find({}).sort([['_id', -1]] ))
    return records

# EMQX Broker post thump to API server
@thump.post("/api/emqx/thump/")
async def broker_post_thump(thump: Thump):
    thump = dict(thump)
    thump["time"] = datetime.now()
    _id = collection_thump.insert_one(thump)
    thump = thumps_serializer(collection_thump.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": thump}