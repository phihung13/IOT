from fastapi import APIRouter, Depends
from models.user_model import *
from schemas.schema_digit import digit_serializer, digits_serializer
from config.db import *
from datetime import datetime
from auth import auth
from emqx.http_publish import pub_digit

# digit = APIRouter(dependencies=[Depends(auth.validate_api_key)])
digit = APIRouter()

# POST method to send digit to server
@digit.post("/api/digit/")
async def post_create_digit(digit: Digit):
    digit = dict(digit)
    result = pub_digit(device_name= digit["device_name"], digit=digit["digit"])
    return {"status": "Ok","data": result}

# GET method to send digit to server
@digit.get("/api/digit/")
async def get_create_digit(device_name: str, digit: int ): 
    result = pub_digit(device_name= device_name, digit= digit)
    return {"status": "Ok","data": result}


@digit.get("/api/get_all_digit")
async def find_all_records():
    records = digits_serializer(collection_digit.find({}).sort([['_id', -1]] ))
    return records

# EMQX Broker post digit to API server
@digit.post("/api/emqx/digit/")
async def broker_post_digit(digit: Digit):
    digit = dict(digit)
    digit["time"] = datetime.now()
    _id = collection_digit.insert_one(digit)
    digit = digits_serializer(collection_digit.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": digit}
