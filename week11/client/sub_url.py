import paho.mqtt.client as mqtt
import time
from datetime import datetime
import urllib.parse


username="device4"
password ="4"
client_id = "client5"
ip = "127.0.0.1"
port = 1883
top_temp = "temp_url"
top_humi = "humi_url"
top_led1 = "led1_url"
top_led2 = "led2_url"
all_url = "all_urlencode"
device_name = "ras_sub"


def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code {}".format(rc))
    client.subscribe(all_url)
    client.subscribe(top_temp)
    client.subscribe(top_humi)
    client.subscribe(top_led1)
    client.subscribe(top_led2)

    
def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")
     
def on_message(client, userdata, msg):
    if msg.topic == all_url:
        all_urlencode = urllib.parse.parse_qs(msg.payload)
        print("topic all_urlencode: {}".format(all_urlencode))

    if msg.topic == top_temp:
        temp = urllib.parse.parse_qs(msg.payload)
        print("topic temp_url: {}".format(temp))
    
    if msg.topic == top_humi:
        humi = urllib.parse.parse_qs(msg.payload)
        print("topic HUMI: {}".format(humi))

    if msg.topic == top_led1:
        led1 = urllib.parse.parse_qs(msg.payload)
        print("topic led1: {}".format(led1))

    if msg.topic == top_led2:
        led2 = urllib.parse.parse_qs(msg.payload)
        print("topic led2: {}".format(led2))
    
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set(username=username, password= password)
client.connect(ip, port, 60)
client.loop_forever()