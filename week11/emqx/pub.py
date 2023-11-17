import paho.mqtt.client as mqtt
from time import sleep
from random import randint
import json
from datetime import datetime

username="http"
password ="http"
client_id = "http"
ip = "127.0.0.1"
port = 1883
top_temp = "temp"
top_humi = "humi"
top_led1 = "led1"
top_led2 = "led2"
top_ultra = "ultra"
top_rotary = "rotary"
top_all = "all"

def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code {}".format(rc))

def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")

client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.username_pw_set(username=username, password= password)
client.connect(ip, port, 60)

def pub_all(device_name: str, data: dict):
    data = {
        "device_name": device_name,
        "data": data
    }
    payload = json.dumps(data)
    print("payload all:", payload)
    try:
        client.publish(topic=top_all, payload= payload, retain=True)
        return data
    except:
        return "Error"


def pub_temp(device_name: str, temp: int):
    data = {
        "device_name": device_name,
        "temp": temp,
    }
    payload = json.dumps(data)
    print("payload temp: ", payload)
    try:
        client.publish(topic=top_temp, payload= payload, retain=True)
        return data
    except:
        return "Error"


def pub_humi(device_name: str, humi: int):
    data = {
        "device_name": device_name,
        "humi": humi,
    }
    payload = json.dumps(data)
    print(payload)
    try:
        client.publish(topic=top_humi, payload= payload, retain=True)
        return data
    except:
        return "Error"

 
def pub_led1(device_name: str, led1: bool):
    data = {
        "device_name": device_name,
        "led1": led1,
    }
    payload = json.dumps(data)
    print(payload)
    try:
        client.publish(topic=top_led1, payload= payload, retain=True)
        return data
    except:
        return "Error"

def pub_led2(device_name: str, led2: bool):
    data = {
        "device_name": device_name,
        "led2": led2,
    }
    payload = json.dumps(data)
    print(payload)
    try:
        client.publish(topic=top_led2, payload= payload, retain=True)
        return data
    except:
        return "Error"
    
def pub_ultra(device_name: str, ultra: int):
    data = {
        "device_name": device_name,
        "ultra": ultra,
    }
    payload = json.dumps(data)
    print(payload)
    try:
        client.publish(topic=top_ultra, payload= payload, retain=True)
        return data
    except:
        return "Error"
    
def pub_rotary(device_name: str, rotary: int):
    data = {
        "device_name": device_name,
        "rotary": rotary,
    }
    payload = json.dumps(data)
    print(payload)
    try:
        client.publish(topic=top_rotary, payload= payload, retain=True)
        return data
    except:
        return "Error"