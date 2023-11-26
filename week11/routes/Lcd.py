from fastapi import APIRouter, Depends
from models.user_model import *
from schemas.schema_lcd import lcd_serializer, lcds_serializer
from config.db import *
from datetime import datetime
from auth import auth
from emqx.http_publish import pub_lcd

# lcd = APIRouter(dependencies=[Depends(auth.validate_api_key)])
lcd = APIRouter()

# POST method to send lcd to server
@lcd.post("/api/lcd/")
async def post_create_lcd(lcd: Lcd):
    lcd = dict(lcd)
    result = pub_lcd(device_name= lcd["device_name"], lcd=lcd["lcd"])
    return {"status": "Ok","data": result}

# GET method to send lcd to server
@lcd.get("/api/lcd/")
async def get_create_lcd(device_name: str, lcd: str ): 
    result = pub_lcd(device_name= device_name, lcd= lcd)
    return {"status": "Ok","data": result}


@lcd.get("/api/get_all_lcd")
async def find_all_records():
    records = lcds_serializer(collection_lcd.find({}).sort([['_id', -1]] ))
    return records

# EMQX Broker post lcd to API server
@lcd.post("/api/emqx/lcd/")
async def broker_post_lcd(lcd: Lcd):
    lcd = dict(lcd)
    lcd["time"] = datetime.now()
    _id = collection_lcd.insert_one(lcd)
    lcd = lcds_serializer(collection_lcd.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": lcd}
