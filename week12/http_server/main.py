from fastapi import FastAPI
from mqtt_publish import *
from datetime import datetime
from time import sleep
from models import user_models as db_type

app = FastAPI()

@app.get("/")
async def hello():
    return {"message": "OK"}


@app.post("/api/post_temmp")
async def post_temp(temp: int, t: datetime, device: str):
    print("time", t)
    result = pub_temp(device_name= device, time= t, temp= temp)
    if result == "OK":
        return {"message": "OK"}
    else: 
        return {"message": "fail"}
    

@app.post("/api/temp")
async def broker_post_temp(temp: db_type.Temp):
    # _id = collection_temp.insert_one(dict(temp))
    # temp = temps_serializer(collection_temp.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": temp}
    