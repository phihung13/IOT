import paho.mqtt.client as mqtt
import time
from datetime import datetime

username="pi"
password ="pi"
client_id = "client2"
ip = "127.0.0.1"
port = 1883
top_temp = "temp"
top_humi = "humi"
top_led1 = "led1"
top_led2 = "led2"
all_top = "all"
device_name = "ras_pub"


def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code {}".format(rc))
    client.subscribe("temp")
    client.subscribe("humi")
    client.subscribe("led1")
    client.subscribe("led2")

    
def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")
     
def on_message(client, userdata, msg):
    if msg.topic == 'temp':
        temp = msg.payload.decode()
        print("topic TEMP: {}".format(temp))
    
    if msg.topic == 'humi':
        humi = msg.payload.decode()
        print("topic HUMI: {}".format(humi))

    if msg.topic == 'led1':
        led1 = msg.payload.decode()
        print("topic led1: {}".format(led1))

    if msg.topic == 'led2':
        led2 = msg.payload.decode()
        print("topic led2: {}".format(led2))

    
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set(username=username, password= password)
client.connect(ip, port, 60)
client.loop_forever()