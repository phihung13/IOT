from datetime import datetime
from time import sleep
# from grove.display.jhd1802 import JHD1802
# from seeed_dht import DHT
from urllib import request, parse
import random


# SENSOR = DHT('11', 18)

api_key_write = "6DHOQHIB7LA73MKR"    


def make_param_thingspeak(TEMPERATURE, HUMIDITY, RANDOM):
    params = parse.urlencode({'field1':TEMPERATURE,'field2':HUMIDITY, 'field3':RANDOM}).encode()
    return params


def thing_speak_post(params): 
    req = request.Request('https://api.thingspeak.com/update', method="POST")
    req.add_header("Content-Type","application/x-www-form-urlencoded")
    req.add_header("X-THINGSPEAKAPIKEY", api_key_write)
    r = request.urlopen(req, data=params)
    respone_data=r.read()
    return respone_data

while True:
    try:
        now = datetime.now()
        # humi, temp = SENSOR.read()
        random_value = random.randrange(0, 100, 1)
        buzz = 1
        
        print("TEMP: {}".format(random_value))
        print("HUMIDITY: {}".format(random_value))
        print("RANDOM VALUE: {}".format(buzz))
        
        params_thingspeak=make_param_thingspeak(random_value, random_value, buzz)
        thing_speak_post(params_thingspeak)
        
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        sleep(20)
            
    except:
        print('KHONG CO INTERNET \n KIEM TRA VA THU LAI')
        sleep(2)