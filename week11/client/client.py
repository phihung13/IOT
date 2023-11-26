from urllib import request, parse
from time import sleep
import random
import json
from datetime import datetime
# from seeed_dht import DHT
# from gpiozero import LED


# SENSOR = DHT('11', 18)
# led1 = LED(5)
# led2 = LED(6)

def create_body(device_name: str,tem: int, humi: int, led1: bool, led2: bool):
    data ={
        "device_name": device_name,
        "data": {
            "tem": tem,
            "humi": humi,
            "led1": led1,
            "led2": led2
        }
    }
    params = data.encode()
    print(params)
    return params

def post_method(body):
    req = request.Request('http://127.0.0.1:8000/api', method="POST")
    req.add_header('Content-Type','application/json')
    req.add_header('accept','application/json')
    req.add_header('X-API-KEY','12345678')
    r = request.urlopen(req, data= body)
    respone_data = r.read()
    print(respone_data)
    return respone_data

while True:
    # humi, tem = SENSOR.read()
    device_name = "Master NODE"
    time = datetime.now()
    tem = random.randint(0,100)
    humi = random.randint(0,100)
    led1 = True
    led2 = False
    body = create_body(device_name, time, tem, humi, led1, led2)
    post_method(body)
    sleep(20)