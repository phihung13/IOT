import paho.mqtt.client as mqtt
from time import sleep
from random import randint
import urllib.parse
from datetime import datetime
# from seeed_dht import DHT
# from gpiozero import LED

username="device2"
password ="2"
client_id = "client2"
ip = "127.0.0.1"
port = 1883
top_temp = "temp_url"
top_humi = "humi_url"
top_led1 = "led1_url"
top_led2 = "led2_url"
all_top = "all_urlencode"
device_name = "ras_pub"

# SENSOR = DHT('11', 18)
# led1 = LED(5)
# led2 = LED(6)

led1 = True
led2 = True
humi = 2
temp = 4

def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code {}".format(rc))

def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")

client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.username_pw_set(username=username, password= password)
client.connect(ip, port, 60)

def pub_all_url(timedevice_name: str, time: datetime, temp: int, humi: int, led1: bool, led2: bool):
    data = {
        "device_name": device_name,
        "time": str(time),
        "temp": temp,
        "humi": humi,
        "led1": led1,
        "led2": led2,
    }
    url_encoded_data = urllib.parse.urlencode(data)
    print(url_encoded_data)
    client.publish(topic=all_top, payload= url_encoded_data, retain=True)

def pub_temp_url(device_name: str, time: datetime, temp: int):
    data = {
        "device_name": device_name,
        "temp": temp,
        "time": str(time),
    }
    url_encoded_data = urllib.parse.urlencode(data)
    print(url_encoded_data)
    client.publish(topic=top_temp, payload= url_encoded_data, retain=True)

def pub_humi_url(device_name: str, time: datetime, humi: int): 
    data = {
        "device_name": device_name,
        "humi": humi,
        "time": str(time),
    }
    url_encoded_data = urllib.parse.urlencode(data)
    print(url_encoded_data)
    client.publish(topic=top_humi, payload= url_encoded_data, retain=True)

def pub_led1_url(device_name: str, time: datetime,  led1: bool):
    data = {
        "device_name": device_name,
        "led1": led1,
        "time": str(time),
    }
    url_encoded_data = urllib.parse.urlencode(data)
    print(url_encoded_data)
    client.publish(topic=top_led1, payload= url_encoded_data, retain=True)

def pub_led2_url(device_name: str, time: datetime,  led2: bool):
    data = {
        "device_name": device_name,
        "led2": led2,
        "time": str(time),
    }
    url_encoded_data = urllib.parse.urlencode(data)
    print(url_encoded_data)
    client.publish(topic=top_led2, payload= url_encoded_data, retain=True)

i = 0
while True:
    time = datetime.now()
    if i%2 == 0:
        led1 = True
        led2 = True
    else: 
        led1 = False
        led2 = False

    # humi, temp = SENSOR.read()
    i = i+1 
    pub_all_url(device_name, time, temp, humi, led1, led2)
    pub_temp_url(device_name, time, temp)
<<<<<<< HEAD
    pub_humi_url(device_name, time, humi)
    pub_led1_url(device_name, time, led1)
    pub_led2_url(device_name, time, led2)
    time.sleep(5)
=======
    # pub_humi_url(device_name, time, humi)
    # pub_led1_url(device_name, time, led1)
    # pub_led2_url(device_name, time, led2)
    sleep(15)
>>>>>>> 36ad739932ab238d1a8910c79a21cca5219fd02d
