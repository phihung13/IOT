import paho.mqtt.client as mqtt
from time import sleep
from random import randint
import json
from datetime import datetime

username="http"
password ="http"
client_id = "http"

IP_HTTP_SERVER = "192.168.1.14"
PORT = 1883

top_temp = "temp"
top_humi = "humi"
top_led1 = "led1"
top_led2 = "led2"
top_ledstick = "ledstick"
top_digit = "digit"
top_sonic = "sonic"
top_light = "light"
top_lcd = "lcd"
top_thump = "thump"
top_all = "all"

def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code {}".format(rc))

def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")

client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.username_pw_set(username=username, password= password)
client.connect(IP_HTTP_SERVER, PORT, 60)

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
    

def pub_ledstick(device_name: str, ledstick: int):
    data = {
        "device_name": device_name,
        "ledstick": ledstick,
    }
    payload = json.dumps(data)
    print(payload)
    try:
        client.publish(topic=top_ledstick, payload= payload, retain=True)
        return data
    except:
        return "Error"
    

def pub_digit(device_name: str, digit: int):
    data = {
        "device_name": device_name,
        "digit": digit,
    }
    payload = json.dumps(data)
    print(payload)
    try:
        client.publish(topic=top_digit, payload= payload, retain=True)
        return data
    except:
        return "Error"


def pub_sonic(device_name: str, sonic: int):
    data = {
        "device_name": device_name,
        "sonic": sonic,
    }
    payload = json.dumps(data)
    print(payload)
    try:
        client.publish(topic=top_sonic, payload= payload, retain=True)
        return data
    except:
        return "Error"


def pub_light(device_name: str, light: int):
    data = {
        "device_name": device_name,
        "light": light,
    }
    payload = json.dumps(data)
    print(payload)
    try:
        client.publish(topic=top_light, payload= payload, retain=True)
        return data
    except:
        return "Error"
    

def pub_lcd(device_name: str, lcd: int):
    data = {
        "device_name": device_name,
        "lcd": lcd,
    }
    payload = json.dumps(data)
    print(payload)
    try:
        client.publish(topic=top_lcd, payload= payload, retain=True)
        return data
    except:
        return "Error"
    
    
def pub_thump(device_name: str, thump: int):
    data = {
        "device_name": device_name,
        "thump": thump,
    }
    payload = json.dumps(data)
    print(payload)
    try:
        client.publish(topic=top_thump, payload= payload, retain=True)
        return data
    except:
        return "Error"