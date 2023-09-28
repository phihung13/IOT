import paho.mqtt.client as mqtt
from time import sleep
# from gpiozero import LED
# from grove.display.jhd1802 import JHD1802
from datetime import datetime
import random
import _thread
from urllib import request, parse

# buzzer = Buzzer(12)
# led = LED(5)
# relay = LED(16)
# lcd = JHD1802()

client_ID = "Aw0OCR0kLyUdCiIFOBQXKzU"
username = "Aw0OCR0kLyUdCiIFOBQXKzU"
password = "qniEYvSqFO/9UO6QM3Auh7sI"

client1_ID = "BBk4MjMwJBAMOxIROC4tOzI"
username1 = "BBk4MjMwJBAMOxIROC4tOzI"
password1 = "Guxn0gYvKY2K7h+292uq1iwt"

def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code {}".format(rc))
    channel_ID = "2277824"
    client.subscribe("channels/%s/subscribe/fields/field1"%(channel_ID))
    client.subscribe("channels/%s/subscribe/fields/field2"%(channel_ID))
    client.subscribe("channels/%s/subscribe/fields/field3"%(channel_ID))
    client.subscribe("channels/%s/subscribe/fields/field4"%(channel_ID))

def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")
    
def mode(message):
    print("==CONTROLL PHYSICAL DEVICE==")
    if message.topic == 'channels/2277824/subscribe/fields/field1':
        mode = message.payload.decode()
        # print("MODE: {}".format(mode))
        # lcd.setCursor(0,0)
        # lcd.write('mode:{}C'.format(mode))
        if mode == "1":
            print("MODE: Auto")
            return True
        else: 
            print("MODE: Manu")
            return False  

def on_message(client, userdata, message):

    MODE = bool(mode(message))

    if message.topic == 'channels/2277824/subscribe/fields/field2':
        if MODE == False:
            led = message.payload.decode()
            # lcd.setCursor(0,9)
            # lcd.write('LED:{}%'.format(led))
            print("LED: {}".format(led))
            # if int(led) == 1:
            #     led.on()
            # if int(led) == 0:
            #     led.off()

    if message.topic == 'channels/2277824/subscribe/fields/field3':
        if MODE == False:
            buz = message.payload.decode()
            # lcd.setCursor(0,9)
            # lcd.write('BUZ:{}%'.format(buz))
            print("BUZ: {}".format(buz))
            # if int(buz) == 1:
            #     buzzer.off()
            # if int(buz) == 0:
            #     buzzer.beep()

    if message.topic == 'channels/2277824/subscribe/fields/field4':
        if MODE == False:
            rl = message.payload.decode()
            # lcd.setCursor(0,9)
            # lcd.write('RELAY:{}%'.format(rl))
            print("RELAY: {}".format(rl))
            # if int(rl) == 1:
            #     relay.off()
            # if int(rl) == 0:
            #     relay.off()
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time)

def get_data_from_server():    
    client = mqtt.Client(client_id=client_ID)
    client.on_connect = on_connect
    # client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.username_pw_set(username , password )
    client.connect("mqtt3.thingspeak.com", 1883, 60)
    client.loop_forever()
    
def mqtt_publish_data_to_server():

    client = mqtt.Client(client_id=client1_ID)
    client.username_pw_set(username=username1 , password=password1 )
    client.connect("mqtt3.thingspeak.com", 1883, 60)

    while True:
        print("==SEND DATA TO THINGSPEAK SERVER==")
        random_tem = random.randint(0, 100)
        random_humi = random.randint(0, 100)
        channel_ID = "2277824"
        print("TEM :", random_tem)
        print("HUMI: ", random_humi)
        client.publish("channels/%s/publish" %(channel_ID), "field5=%s&status=MQTTPUBLISH " %(random_tem))
        client.publish("channels/%s/publish" %(channel_ID), "field6=%s&status=MQTTPUBLISH " %(random_humi))

        sleep(10)


def http_post_data_to_server():
    def make_param_thingspeak(humi,temp):
        params = parse.urlencode({'field5':humi,'field6':temp }).encode()
        return params

    def thingspeak_post(params):
        api_key_write = "ZX3DK0TRD4HT2VQE"
        req = request.Request('http://api.thingspeak.com/update',method="POST")
        req.add_header("Content-Type","application/x-www-form-urlencoded")
        req.add_header("X-THINGSPEAKAPIKEY",api_key_write)
        r = request.urlopen(req,data= params)
        respone_data = r.read()
        return respone_data

    
    while True:
        try:
            humi = random.randint(70,100)
            temp = random.randint(25,45)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("do am",humi)
            print("nhiet do",temp)
            params_thingspeak = make_param_thingspeak(humi,temp)
            thingspeak_post(params_thingspeak)
            print("Current Time =", current_time)
            sleep(20)
            
        except:
            print('KHONG CO INTERNET \n KIEM TRA VA THU LAI')
            sleep(2)

# if __name__ == "main":

# second_thread = _thread.start_new_thread(mqtt_publish_data_to_server, ())

second_thread = _thread.start_new_thread(http_post_data_to_server, ())

get_data_from_server()