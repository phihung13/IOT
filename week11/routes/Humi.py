from fastapi import APIRouter, Depends
from models.user_model import *
from schemas.schema_humi import humi_serializer, humis_serializer
from config.db import *
from datetime import datetime
from auth import auth
from emqx.http_publish import pub_humi

# humi = APIRouter(dependencies=[Depends(auth.validate_api_key)])
humi = APIRouter()

# POST method to send HUMI to server
@humi.post("/api/humi/")
async def post_create_humi(humi: Humi):
    humi = dict(humi)
    result = pub_humi(device_name= humi["device_name"], humi=humi["humi"])
    return {"status": "Ok","data": result}

# GET method to send HUMI to server
@humi.get("/api/humi/")
async def get_create_humi(device_name: str, humi: int ): 
    result = pub_humi(device_name= device_name, humi= humi)
    return {"status": "Ok","data": result}


@humi.get("/api/get_all_humi")
async def find_all_records():
    records = humis_serializer(collection_humi.find({}).sort([['_id', -1]] ))
    return records

# EMQX Broker post HUMI to API server
@humi.post("/api/emqx/humi/")
async def broker_post_humi(humi: Humi):
    humi = dict(humi)
    humi["time"] = datetime.now()
    _id = collection_humi.insert_one(humi)
    humi = humis_serializer(collection_humi.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": humi}
