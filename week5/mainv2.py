import paho.mqtt.client as mqtt
from time import sleep
# from gpiozero import LED
# from gpiozero import Buzzer
# from grove.display.jhd1802 import JHD1802
from datetime import datetime
import random
import _thread
from urllib import request, parse
# from seeed_dht import DHT
from datetime import datetime, time
import json

# buzzer = Buzzer(12)
# led = LED(5)
# relay = LED(16)
# lcd = JHD1802()
# SENSOR = DHT('11', 18)

start_time = 18  # 18:00
end_time = 22 

client_ID = "Aw0OCR0kLyUdCiIFOBQXKzU"
username = "Aw0OCR0kLyUdCiIFOBQXKzU"
password = "qniEYvSqFO/9UO6QM3Auh7sI"

# Thread 1, use mqtt protocol to received data from MQTT broker
def MQTT():
    # connect to MQTT broker
    def on_connect(client, userdata, flags, rc):
        print("Connected With Result Code {}".format(rc))
        channel_ID = "2277824"
        # SUBSCRIBE 4 CHANNEL OF MQTT BROKER
        # FIELD 1 HAS 2 MODE: AUTO AND MANUAL
        client.subscribe("channels/%s/subscribe/fields/field1"%(channel_ID))
        # FIELD 2 IS SIGNAL CONTROL LED
        client.subscribe("channels/%s/subscribe/fields/field2"%(channel_ID))
        # FIELD 3 IS SIGNAL CONTROL BUZZER
        client.subscribe("channels/%s/subscribe/fields/field3"%(channel_ID))
        # FIELD 4 IS SIGNAL CONTROL RELAY
        client.subscribe("channels/%s/subscribe/fields/field4"%(channel_ID))

    # DISCONNECT MQTT BROKER
    def on_disconnect(client, userdata, rc):
        print("Disconnected From Broker")
    
    #  CHECK MODE IN THE MESSAGE RECEIVED FROM BROKER
    def mode(message):
        print("")
        print("******")
        print("==CURRENT MODE:==")

        # IF MODE EQUAL 1 IS AUTO
        # IF MODE EQUAL 0 IS MANUAL
        if message.topic == 'channels/2277824/subscribe/fields/field1':
            mode = message.payload.decode()

            # PRINT MODE TO LCD SCREEN
            # print("MODE: {}".format(mode))
            # lcd.setCursor(0,0)
            # lcd.write('mode:{}'.format(mode))

            # WHEN SWITCHING THE MODE ALL DEVICES SHOULD BE TURNED OFF 
            # AND THEN WILL BE RE-OPERATIVE ACCORDING TO THE MODE DESIGNATED 
            # relay.off()
            # led.off()
            # buzzer.off()
            if mode == "1":
                print("AUTO")
                return True
            else: 
                print("MANUAL")
                return False  

    def on_message(client, userdata, message):       
        # READ DATA FROM BROKER TO CONTROL PHYSICAL DEVICE
        # First, we need to check the mode. 
        # If it is manual, it allows controlling the device through the web interface.
        # If it is auto, it can be controlled according to pre-set requirements.
        MODE = bool(mode(message))
        # humi, temp = SENSOR.read()

        if message.topic == 'channels/2277824/subscribe/fields/field2':
            if MODE == False:
                st_led = message.payload.decode()
                # lcd.setCursor(0,9)
                # lcd.write('LED:{}'.format(st_led))
                print("LED: {}".format(st_led))
                if int(st_led) == 1:
                    print("LED ON")
                    # led.on()
                if int(st_led) == 0:
                    print("LED OFF")
                    # led.off()

        if message.topic == 'channels/2277824/subscribe/fields/field3':
            if MODE == False:
                buz = message.payload.decode()
                # lcd.setCursor(0,9)
                # lcd.write('BUZ:{}'.format(buz))
                print("BUZ: {}".format(buz))
                if int(buz) == 1:
                    print("BUZZER ON")
                    # buzzer.beep()
                if int(buz) == 0:
                    print("BUZZER OFF")
                    # buzzer.off()

        if message.topic == 'channels/2277824/subscribe/fields/field4':
            if MODE == False:
                rl = message.payload.decode()
                # lcd.setCursor(0,9)
                # lcd.write('RELAY:{}'.format(rl))
                print("RELAY: {}".format(rl))
                if int(rl) == 1:
                    print("RELAY OFF")
                    # relay.on()
                if int(rl) == 0:
                    print("RELAY ON")
                    # relay.off()

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current time of mqtt:", current_time)
   
    client = mqtt.Client(client_id=client_ID)
    client.on_connect = on_connect
    # client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.username_pw_set(username , password )
    client.connect("mqtt3.thingspeak.com", 1883, 60)
    client.loop_forever()


def HTTP():
    G_mode = "1"

    # HANDLE PARAMETER TO POST TO SERVER
    def make_param_thingspeak(humi,temp):
        params = parse.urlencode({'field5':temp,'field6':humi}).encode()
        return params
    
    # POST DATA TO SERVER
    def thingspeak_post(params):
        api_key_write = "ZX3DK0TRD4HT2VQE"
        req = request.Request('http://api.thingspeak.com/update',method="POST")
        req.add_header("Content-Type","application/x-www-form-urlencoded")
        req.add_header("X-THINGSPEAKAPIKEY",api_key_write)
        r = request.urlopen(req,data= params)
        respone_data = r.read()
        return respone_data

    # GET DATA FROM SERVER
    def thingspeak_get_data():
        api_key_read = "RR6PXG8KID1VQ6BG"
        channel_ID = "2277824"

        req = request.Request("https://api.thingspeak.com/channels/2277824/feeds.json?api_key=RR6PXG8KID1VQ6BG", method="GET")
        r = request.urlopen(req)
        response_data = r.read().decode()
        response_data = json.loads(response_data)

        data = response_data["feeds"]
        data_c = response_data["channel"]
        return data, data_c
    
    while True:
        now = datetime.now()
        try:
            # SET UP DEVICE RUN IN AUTO MODE
            for i in range(10):                
                data, data_c = thingspeak_get_data()
                s_mode = data[len(data)-1]['field%s'%(1)]

                if s_mode != None:
                    print("\n    ******")
                    G_mode = s_mode
                    print("CURRENT MODE: ", G_mode)
                    print("    ******") 

                if G_mode == "1":
                    r_temp = random.randrange(0,50)
                    r_humi = random.randrange(0,100)
                    print(f"\nTIME NOW IN AUTO MODE: {now.hour}")
                    if start_time <= now.hour <= end_time:
                        print(" - LED STATUS: ON")
                        # led.on()
                    else:
                        print(" - LED STATUS: OFF")
                        # led.off()

                    print("\nTEMP READ FROM SENSOR IN AUTO MODE: ", r_temp)
                    if r_temp > 37:
                        print(" - BUZZER STATUS: ON")
                        # buzzer.beep()
                    elif r_temp < 31:
                        print(" - BUZZER STATUS: OFF")
                        # buzzer.off()
                    else:
                        print(" - BUZZER STATUS: NO CHANGE")

                    print("\nHUMI READ FROM SENSOR IN AUTO MODE: ", r_humi)
                    if r_humi > 90:
                        print(" - RELAY STATUS: ON")
                        # relay.on()
                    elif r_humi < 60:
                        print(" - RELAY STATUS: OFF")
                        # relay.off()
                    else:
                        print(" - RELAY STATUS: NO CHANGE")

                sleep(2)

            # GET DATA FROM SENSOR AFTER POST TO SERVER EACH 20S
            # humi, temp = SENSOR.read()
            r_temp = random.randrange(0,100)
            r_humi = random.randrange(0,100)
            # now = datetime.now()print("======================")
            # print("HUMI POST: ",humi)
            # print("TEMP POST: ",temp)
            print("\n**************************")
            print("After 20s post data to server")
            print("HUMI POST: ",r_humi)
            print("TEMP POST: ",r_temp)
            current_time = now.strftime("%H:%M:%S")
            params_thingspeak = make_param_thingspeak(r_humi,r_temp)
            thingspeak_post(params_thingspeak)
            print("Current Time user Post HTTP =", current_time)
            print("**************************\n")

        except:
            print('KHONG CO INTERNET \n KIEM TRA VA THU LAI')
            sleep(2)

# CREATE NEW THREAD TO RUN HTTP POTOCOL
second_thread = _thread.start_new_thread(HTTP, ())

# RUN MQTT PTOTOCOL
MQTT()