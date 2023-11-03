import urllib.parse
import paho.mqtt.client as mqtt
import time
from random import randint
import json
from datetime import datetime

username="device1"
password ="1"
client_id = "client1"
ip = "127.0.0.1"
port = 1883
top_test = "all"
device_name = "ras_pub"


def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code {}".format(rc))

def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")

client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.username_pw_set(username=username, password= password)
client.connect(ip, port, 60)

def pub_test():
    data1 = randint(0,100) 
    data2 = randint(0,100)
    t = datetime.now()
    print(t)
    data = {
        "device_name": device_name,
        "time": str(t),
        "temp": data1,
        "humi": data2,
        "led1": True,
        "led2": False,
    }

    url_encoded_data = urllib.parse.urlencode(data)
    print(url_encoded_data)
    client.publish(topic=top_test, payload= url_encoded_data, retain=True)



while True:
    pub_test()
    time.sleep(5)