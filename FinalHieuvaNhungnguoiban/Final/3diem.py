import json
from urllib import request, parse
from time import sleep
from gpiozero import LED
from seeed_dht import DHT

led1 = LED(18)
led2 = LED(16)
dht = DHT('11',5)
mode = 0
i=0

def make_param_thingspeak(temp, humi):
    params = parse.urlencode({'field1': temp, 'field2': humi}).encode()
    return params

def thingspeak_post(params):
    api_key_write = "BWXKPCXW1JXZ8F63"
    req = request.Request('http://api.thingspeak.com/update',method="POST")
    req.add_header("Content-Type","application/x-www-form-urlencoded")
    req.add_header("X-THINGSPEAKAPIKEY",api_key_write)
    request.urlopen(req, data=params)

def thingspeak_get():
    status = list()
    req = request.Request("https://api.thingspeak.com/channels/2340152/feeds.json?api_key=9B0XBM2LBT12D03J",method="GET")
    r = request.urlopen(req)
    response_data = r.read().decode()
    response_data = json.loads(response_data)
    value = response_data.get("feeds")[-1]
    status.append(value.get("field1"))
    status.append(value.get("field2"))
    status.append(value.get("field3"))
    return status

while True:
    status = thingspeak_get()
    humi, temp = dht.read()
    
    params_thingspeak = make_param_thingspeak(temp, humi)
    thingspeak_post(params_thingspeak)

    print('nhiet do = {}C va do am = {}%'.format(temp, humi))

    if status[2] == '0':
        mode = 0
    elif status[2] == '1':
        mode = 1
    
    if mode == 0:
        print("Auto")
            
        if temp > 37:
            led1.on()
        elif temp < 31:
            led1.off()

        if humi > 90:
            led2.on()
        elif humi < 60:
            led2.off()
        i=1

    if mode == 1:
        print("Manual")
        
        if i==1:
            led1.off()
            led2.off()
            i=0
        
        if status[1] == '1':
            led1.on()
            print("LED 1 on")
        if status[1] == '0':
            led1.off()

        if status[2] == '1':
            led2.on()
            print("LED 2 on")
        if status[2] == '0':
            led2.off()
        
        sleep(1)