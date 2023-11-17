import paho.mqtt.client as mqtt
import time
from datetime import datetime

username="sub1"
password ="1"
client_id = "sub1"
ip = "127.0.0.1"
port = 1883
top_temp = "temp"
top_humi = "humi"
top_led1 = "led1"
top_led2 = "led2"
all_top = "all"
device_name = "ras_sub"


def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code {}".format(rc))
    client.subscribe(all_top)
    client.subscribe(top_temp)
    client.subscribe(top_humi)
    client.subscribe(top_led1)
    client.subscribe(top_led2)

    
def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")
     
def on_message(client, userdata, msg):
    if msg.topic == all_top:
        all_json = msg.payload.decode()
        print("topic all_json: {}".format(all_json))

    if msg.topic == top_temp:
        temp = msg.payload.decode()
        print("topic TEMP: {}".format(temp))
    
    if msg.topic == top_humi:
        humi = msg.payload.decode()
        print("topic HUMI: {}".format(humi))

    if msg.topic == top_led1:
        led1 = msg.payload.decode()
        print("topic led1: {}".format(led1))

    if msg.topic == top_led2:
        led2 = msg.payload.decode()
        print("topic led2: {}".format(led2))

    
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set(username=username, password= password)
client.connect(ip, port, 60)
client.loop_forever()