import paho.mqtt.client as mqtt
import random
from time import sleep


client1_ID = "LhkoBiYHGR0HJRUGFi8FFhs"
username1 = "LhkoBiYHGR0HJRUGFi8FFhs"
password1 = "Xb7TXEJs7FCwGCn32yCHcdDE"

client = mqtt.Client(client_id=client1_ID)
client.username_pw_set(username=username1 , password=password1)
client.connect("mqtt3.thingspeak.com", 1883, 60)

def thing(tem, humi):
    channel_ID = "2277824"
    client.publish("channels/%s/publish" %(channel_ID), "field5=%s&status=MQTTPUBLISH " %(tem))
    client.publish("channels/%s/publish/" %(channel_ID), "field6=%s&status=MQTTPUBLISH" %(humi))

while True:
    print("==SEND DATA TO THINGSPEAK SERVER==")
    random_tem = random.randint(0, 100)
    random_humi = random.randint(0, 100)
    print("TEM :", random_tem)
    print("TEM :", random_humi)

    thing(random_tem, random_humi)

    sleep(20)