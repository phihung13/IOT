import paho.mqtt.client as mqtt
import time
from random import randint
import json
from datetime import datetime
from seeed_dht import DHT
from gpiozero import LED

username="device1"
password ="1"
client_id = "client1"
ip = "192.168.1.21"
port = 1883
top_temp = "temp"
top_humi = "humi"
top_led1 = "led1"
top_led2 = "led2"
all_top = "all_json"
device_name = "ras_pub"

SENSOR = DHT('11', 18)
led1 = LED(5)
led2 = LED(6)


def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code {}".format(rc))

def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")

client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.username_pw_set(username=username, password= password)
client.connect(ip, port, 60)

def pub_all(device_name: str, time: datetime, temp: int, humi: int, led1: bool, led2: bool):
    data = {
        "device_name": device_name,
        "time": str(time),
        "temp": temp,
        "humi": humi,
        "led1": led1,
        "led2": led2,
    }
    payload = json.dumps(data)
    print(payload)
    client.publish(topic=all_top, payload= payload, retain=True)


def pub_temp(device_name: str, time: datetime, temp: int):
    data = {
        "device_name": device_name,
        "time": str(time),
        "temp": temp,
    }
    payload = json.dumps(data)
    print(payload)
    client.publish(topic=top_temp, payload= payload, retain=True)

def pub_humi(device_name: str, time: datetime, humi: int):
    data = {
        "device_name": device_name,
        "time": str(time),
        "humi": humi,
    }
    payload = json.dumps(data)
    print(payload)
    client.publish(topic=top_humi, payload= payload, retain=True)

def pub_led1(device_name: str, time: datetime,  led1: bool):
    data = {
        "device_name": device_name,
        "time": str(time),
        "led1": led1,
    }
    payload = json.dumps(data)
    print(payload)
    client.publish(topic=top_led1, payload= payload, retain=True)

def pub_led2(device_name: str, time: datetime,  led2: bool):
    data = {
        "device_name": device_name,
        "time": str(time),
        "led2": led2,
    }
    payload = json.dumps(data)
    print(payload)
    client.publish(topic=top_led2, payload= payload, retain=True)
i = 0
while True:
    time = datetime.now()
    i = i+1
    if i%2 == 0:
        led1 = True
        led2 = True
    else: 
        led1 = False
        led2 = False

    humi, temp = SENSOR.read()

    pub_all(device_name, time, temp, humi, led1, led2)
    pub_temp(device_name, time, temp)
    pub_humi(device_name, time, humi)
    pub_led1(device_name, time, led1)
    pub_led2(device_name, time, led2)
    time.sleep(5)