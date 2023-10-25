import paho.mqtt.client as mqtt
from datetime import datetime


username = "DgQVHB0WLwYhFgUzMDkBNAo"
clientId = "DgQVHB0WLwYhFgUzMDkBNAo"
password = "2+1/W2qOMKeMz1wAEgm5j8Re"

# create a new mqtt device and get ID channel replace below
channel_id = "2317304"

# connect to MQTT broker
def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code {}".format(rc))
    # create a new mqtt device and get ID channel replace below
    # SUBSCRIBE 4 CHANNEL OF MQTT BROKER
    # FIELD 1 HAS 2 MODE: AUTO AND MANUAL
    client.subscribe("channels/%s/subscribe/fields/field1"%(channel_id))
    # FIELD 2 IS SIGNAL CONTROL LED
    client.subscribe("channels/%s/subscribe/fields/field2"%(channel_id))
    # FIELD 3 IS SIGNAL CONTROL RELAY
    client.subscribe("channels/%s/subscribe/fields/field3"%(channel_id))
    # FIELD 4 IS SIGNAL CONTROL TEMP
    client.subscribe("channels/%s/subscribe/fields/field4"%(channel_id))
    # FIELD 5 IS SIGNAL CONTROL HUMI
    client.subscribe("channels/%s/subscribe/fields/field5"%(channel_id))

# DISCONNECT MQTT BROKER
def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")

#  CHECK MODE IN THE MESSAGE RECEIVED FROM BROKER
def mode(message):
    
    # IF MODE EQUAL 1 IS AUTO
    # IF MODE EQUAL 0 IS MANUAL
    if message.topic == 'channels/{}/subscribe/fields/field1'.format(channel_id):
        mode = message.payload.decode()
        print("")
        print("******")
        print("==CURRENT MODE:==")
        if mode == "1":
            print("AUTO")
            return True
        else: 
            print("MANUAL")
            return False  

def on_message(client, userdata, message):       
    # GET DATA FROM BROKER TO CONTROL PHYSICAL DEVICE
    # First, we need to check the mode. 
    # If it is manual, it allows controlling the device through the web interface.
    # If it is auto, it can be controlled according to pre-set requirements.

    # check mode from thingspeak server
    MODE = bool(mode(message))

    #  GET LED STATUS
    if message.topic == 'channels/{}/subscribe/fields/field2'.format(channel_id):
        # CONTROL LED MANUAL MODE
        if MODE == False:
            st_led = message.payload.decode()
            print("LED: {}".format(st_led))
            if int(st_led) == 1:
                print("LED ON")
                # led.on()
            if int(st_led) == 0:
                print("LED OFF")
                # led.off()

    # GET RELAY STATUS
    if message.topic == 'channels/{}/subscribe/fields/field3'.format(channel_id):
        # CONTROL RELAY MANUAL MODE
        if MODE == False:
            rl = message.payload.decode()
            print("RELAY: {}".format(rl))
            if int(rl) == 1:
                print("RELAY ON")
                # relay.on()
            if int(rl) == 0:
                print("RELAY OFF")
                # relay.off()
    
    # GET TEM TO CONTROL LED AND PRINT TO LCD
    if message.topic == 'channels/{}/subscribe/fields/field4'.format(channel_id):
        tem = message.payload.decode()
        print("TEM: {}".format(tem))
        # lcd.setCursor(0,0)
        # lcd.write('TEM:{}'.format(tem))
        # LED AUTO ON OFF WITH TEM VALUE
        if MODE == True:
            if int(tem) >= 35:
                print("TEM >= 35")
                # led.on()
            if int(tem) <= 31:
                print("TEM <= 31")
                # led.off()
            

    # GET HUMI TO CONTROL RELAY AND PRINT TO LCD
    if message.topic == 'channels/{}/subscribe/fields/field5'.format(channel_id):
        humi = message.payload.decode()
        print("HUMI: {}".format(humi))
        if MODE == True:
        # lcd.setCursor(0,0)
        # lcd.write('TEM:{}'.format(tem))
        # RELAY AUTO ON OFF WITH HUMI VALUE
            if int(humi) >= 90:
                print("humi >= 90%")
                # relay.on()
            if int(humi) <= 60:
                print("humi <= 60%")
                # relay.off()
            # lcd.setCursor(1,0)
            # lcd.write('HUMI:{}'.format(humi))
            

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Time now in ras 2 (mqtt):", current_time)
    print("===========================")

client = mqtt.Client(client_id=clientId)
client.on_connect = on_connect
# client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set(username , password )
client.connect("mqtt3.thingspeak.com", 1883, 60)
client.loop_forever()