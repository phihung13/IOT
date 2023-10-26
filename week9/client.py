from urllib import request, parse
from time import sleep
import random
import json
from datetime import datetime

def create_body(device_name: str, time: datetime, tem: int, humi: int, led1: bool, led2: bool):
    data ={
        "device_name": device_name,
        "time": str(time),
        "tem": tem,
        "humi": humi,
        "led1": led1,
        "led2": led2
    }
    params = json.dumps(data).encode()
    print(params)
    return params

def create_query(device_name: str, time: datetime, tem: int, humi: int, led1: bool, led2: bool):
    param ={
        "device_name": device_name,
        "tem": tem,
        "humi": humi,
        "led1": led1,
        "led2": led2,
        "time": str(time)
    }
    return param

def post_method(body):
    req = request.Request('http://127.0.0.1:8000/api', method="POST")
    req.add_header('Content-Type','application/json')
    req.add_header('accept','application/json')
    req.add_header('X-API-KEY','12345678')
    r = request.urlopen(req, data= body)
    respone_data = r.read()
    print(respone_data)
    return respone_data

def get_method(query_string):
    query = parse.urlencode(query_string)
    url = "http://127.0.0.1:8000/api/{record}?" + query
    req = request.Request(url, method="GET",)
    req.add_header('Content-Type','application/json')
    req.add_header('accept','application/json')
    req.add_header('X-API-KEY','12345678')
    r = request.urlopen(req)
    respone_data = r.read()
    print(respone_data)
    return respone_data

while True:
    device_name = "ras1"
    time = datetime.now()
    tem = random.randint(0,100)
    humi = random.randint(0,100)
    led1 = True
    led2 = False
    # body = create_body(device_name, time, tem, humi, led1, led2)
    query_string = create_query(device_name, time, tem, humi, led1, led2)
    # post_method(body)
    get_method(query_string)
    sleep(20)