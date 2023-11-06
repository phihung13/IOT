from fastapi import APIRouter
from models.user_model import *
from schemas.record_schema import *
from config.db import *
from datetime import datetime
from fastapi import FastAPI, Body, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from auth import auth
import matplotlib.pyplot as plt
from io import BytesIO
import base64


# record = APIRouter(dependencies=[Depends(auth.validate_api_key)])
record = APIRouter()

# Use POST method to send data to server
@record.post("/api")
async def post_create_record(record: Record):
    _id = collection.insert_one(dict(record))
    record = records_serializer(collection.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": record}

# Use GET method to send data to server
@record.get("/api/{record}")
async def get_create_record(device_name: str, temp: int , humi: int , led1: bool, led2: bool, time: datetime = datetime.now() ):  
    record = {
        "device_name" : device_name,
        "time" : time,
        "temp" : temp,
        "humi" : humi,
        "led1" : led1,
        "led2" : led2,
   }
    _id = collection.insert_one(dict(record))
    record = records_serializer(collection.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": record}


# get all record from server
@record.get("/api/getAll")
async def find_all_records():
    records = records_serializer(collection.find({}).sort([['_id', -1]] ))
    return {"status": "Ok","data": records}


# get the last n records from server
@record.get("/api/getNLast/{n}")
async def get_last_record(number : int):
   number_record = records_serializer(collection.find().sort([['_id', -1]]).limit(number))
   return {"status": "Ok","data": number_record}

@record.get("/api/getTime/{time}")
async def get_record_by_time(start: datetime, end: datetime):

   number_record = records_serializer(collection.find(
    {
        "time": {
            "$gte": start,
            "$lt" : end
        }
    }
   ))
   return {"status": "Ok","data": number_record}

def get_data():
    data = collection.find() 
    temp = []
    humi = []
    time = []
    led1 = []
    led2 = []
    
    for item in data:
        temp.append(item['temp'])  
        humi.append(item['humi'])
        time.append(item['time'])
        led1.append(item['led1'])
        led2.append(item['led2'])
    
    return temp, humi, time, led1, led2

def plot_line_chart(data1, data2,time, led1, led2):
    plt.figure()

    plt.subplot(2, 2, 1)
    plt.plot(time,data1)
    plt.xlabel('Time')
    plt.ylabel('Temp')
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.plot(time,data2)
    plt.xlabel('TIME')
    plt.ylabel('Humi')
    plt.legend()

    plt.subplot(2, 2, 3)
    plt.plot(time,led1)
    plt.xlabel('Time')
    plt.ylabel('Led1')
    plt.legend()

    plt.subplot(2, 2, 4)
    plt.plot(time,led2)
    plt.xlabel('Time')
    plt.ylabel('Led2')
    
    plt.legend()
    plt.suptitle('GRAPH')

    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')
    return img_base64

@record.get("/graph", response_class=HTMLResponse)
def display_graph():
    data1, data2, id_values, trang_thai_led1, trang_thai_led2 = get_data()
    img_base64 = plot_line_chart(data1, data2, id_values, trang_thai_led1, trang_thai_led2)
    
    html_content = f"""
    <html>
    <head>
        <title>GRAPH</title>
        <meta http-equiv="refresh" content="5" >
    </head>
    <body>
        <h1>SHOW DATA</h1>
        <img src="data:image/png;base64,{img_base64}" />
    </body>
    </html>
    """
    return html_content


"""bài 10"""

@record.post("/api/broker")
async def broker_post_record(record: Record):
    _id = collection2.insert_one(dict(record))
    record = records_serializer(collection2.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": record}

@record.post("/api/temp")
async def broker_post_temp(temp: Temp):
    _id = collection_temp.insert_one(dict(temp))
    temp = temps_serializer(collection_temp.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": temp}

@record.post("/api/humi")
async def broker_post_humi(humi: Humi):
    _id = collection_humi.insert_one(dict(humi))
    humi = humis_serializer(collection_humi.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": humi}

@record.post("/api/led1")
async def broker_post_led1(led1: Led1):
    _id = collection_led1.insert_one(dict(led1))
    led1 = led1s_serializer(collection_led1.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": led1}

@record.post("/api/led2")
async def broker_post_led2(led2: Led2):
    print(led2)
    _id = collection_led2.insert_one(dict(led2))
    led2 = led2s_serializer(collection_led2.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": led2}


# Use GET method to send data to server
@record.get("/api/emqx/url")
async def broker_get_record(device_name: str, temp: int , humi: int , led1: bool, led2: bool, time: datetime = datetime.now() ):  
    record = {
        "device_name" : device_name,
        "time" : time,
        "temp" : temp,
        "humi" : humi,
        "led1" : led1,
        "led2" : led2,
   }
    _id = collection2.insert_one(dict(record))
    record = records_serializer(collection2.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": record}

@record.get("/api/emqx/temp")
async def broker_get_temp(device_name: str, temp: int, time: datetime = datetime.now()):
    temp = {
        "device_name" : device_name,
        "time" : time,
        "temp" : temp,
    }
    _id = collection_temp.insert_one(dict(temp))
    temp = temps_serializer(collection_temp.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": temp}

# @record.get("/api/humi")
# async def broker_get_humi(humi: int):
#     print(humi)
#     _id = collection_humi.insert_one(dict(humi))
#     humi = humis_serializer(collection_humi.find({"_id": _id.inserted_id}))
#     return {"status": "Ok","data": humi}

# @record.get("/api/led1")
# async def broker_get_led1(led1: bool):
#     print(led1)
#     _id = collection_led1.insert_one(dict(led1))
#     led1 = led1s_serializer(collection_led1.find({"_id": _id.inserted_id}))
#     return {"status": "Ok","data": led1}

# @record.get("/api/led2")
# async def broker_get_led2(led2: bool):
#     print(led2)
#     _id = collection_led2.insert_one(dict(led2))
#     led2 = led2s_serializer(collection_led2.find({"_id": _id.inserted_id}))
#     return {"status": "Ok","data": led2}