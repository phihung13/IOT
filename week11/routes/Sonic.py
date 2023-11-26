from fastapi import APIRouter, Depends
from models.user_model import *
from schemas.schema_sonic import sonic_serializer, sonics_serializer
from config.db import *
from datetime import datetime
from auth import auth
from emqx.http_publish import pub_sonic

# sonic = APIRouter(dependencies=[Depends(auth.validate_api_key)])
sonic = APIRouter()

# POST method to send sonic to server
@sonic.post("/api/sonic/")
async def post_create_sonic(sonic: Sonic):
    sonic = dict(sonic)
    result = pub_sonic(device_name= sonic["device_name"], sonic=sonic["sonic"])
    return {"status": "Ok","data": result}

# GET method to send sonic to server
@sonic.get("/api/sonic/")
async def get_create_sonic(device_name: str, sonic: int ):  
    result = pub_sonic(device_name= device_name, sonic= sonic)
    return {"status": "Ok","data": result}


@sonic.get("/api/get_all_sonic")
async def find_all_records():
    records = sonics_serializer(collection_sonic.find({}).sort([['_id', -1]] ))
    return records

# EMQX Broker post sonic to API server
@sonic.post("/api/emqx/sonic/")
async def broker_post_sonic(sonic: Sonic):
    sonic = dict(sonic)
    sonic["time"] = datetime.now()
    _id = collection_sonic.insert_one(sonic)
    sonic = sonics_serializer(collection_sonic.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": sonic}