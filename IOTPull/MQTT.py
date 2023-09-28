import paho.mqtt.client as mqtt
import time
# from gpiozero import LED
# from grove.display.jhd1802 import JHD1802
from datetime import datetime

# buzzer = Buzzer(12)
# led = LED(5)
# relay = LED(16)
# lcd = JHD1802()
username = "DQYANRASGyUPDTw8BzEoDTc"
password = "YJBdMVZQSEwOd4DsZv8LtsVJ"


def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code {}".format(rc))
    channel_ID = "2030546"
    client.subscribe("channels/%s/subscribe/fields/field1"%(channel_ID))
    client.subscribe("channels/%s/subscribe/fields/field2"%(channel_ID))
    client.subscribe("channels/%s/subscribe/fields/field3"%(channel_ID))
    client.subscribe("channels/%s/subscribe/fields/field3"%(channel_ID))
    client.publish("channels/%s/publish/" %(channel_ID), "field5=%s&status=MQTTPUBLISH" %(userdata[0]))
    client.publish("channels/%s/publish/" %(channel_ID), "field6=%s&status=MQTTPUBLISH" %(userdata[1]))

def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")
    
    
def on_message(client, userdata, message):
    pass
    # if message.topic == 'channels/2030546/subscribe/fields/field1':
    #     temp = message.payload.decode()[0:2]
    #     print("Nhiet do: {}".format(temp))
    #     lcd.setCursor(0,0)
    #     lcd.write('Temp:{}C'.format(temp))
    #     if int(temp)>=20 and int(temp)<=30:
    #         print("Giu status")
    #     if int(temp)<31:
    #         buzzer.off()
    #     if int(temp)>37:
    #         buzzer.beep()
    
    # if message.topic == 'channels/2030546/subscribe/fields/field2':
    #     humi = message.payload.decode()[0:2]
    #     lcd.setCursor(0,9)
    #     lcd.write('hum:{}%'.format(humi))
    #     print("Do am: {}".format(humi))
    #     if int(humi)>=80 and int(humi)<=90:
    #         print("giu status")
    #     if int(humi)>90:
    #         relay.on()
    #     if int(humi)<60:
    #         relay.off()
    
    # if message.topic == 'channels/2030546/subscribe/fields/field3':
    #     rd = message.payload.decode()[0:3]
    #     rds = rd
    #     lcd.setCursor(1,0)
    #     lcd.write('Random: {}'.format(str(rds)+' '))
    #     print("Random: {}".format(rd))
    #     print('--------------------')
    #     if (int(rd) > 50):
    #         led.on()
    #     else:
    #         led.off()
    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    
client = mqtt.Client("DQYANRASGyUPDTw8BzEoDTc")
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set(username , password )
client.connect("mqtt3.thingspeak.com", 1883, 60)
client.loop_forever()

