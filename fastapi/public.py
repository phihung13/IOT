import paho.mqtt.client as mqtt
from time import sleep
from random import randint
import json

usname = "device2"
psword = "2"
client_ID = "2"
ip = "192.168.1.143"
portt = 1883
topic = "test"


def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code {}".format(rc))

def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")

client = mqtt.Client(client_id=client_ID)
client.on_connect = on_connect
# client.on_disconnect = on_disconnect
client.username_pw_set(username=usname, password=psword)
client.connect(host=ip, port=portt, keepalive=60)

def thingspeak_mqtt(data1, data2):
    dt = {
        "data1": data1,
        "data2": data2
    }
    json_data = json.dumps(dt)
    print(json_data)
    # client.publish("Vidu", json_data)
    client.publish(topic=topic, payload=json_data)

while True:
    # data_random= int
    data_random = randint(0, 50)
    print(data_random)
    thingspeak_mqtt(data_random, data_random)
    sleep(10)