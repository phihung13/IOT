from urllib import request, parse
from time import sleep
from random import randint 
from datetime import datetime


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
        humi = randint(70,100)
        temp = randint(25,45)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("do am",humi)
        print("nhiet do",temp)
        params_thingspeak = make_param_thingspeak(humi,temp)
        thingspeak_post(params_thingspeak)
        sleep(20)
        
    except:
        print('KHONG CO INTERNET \n KIEM TRA VA THU LAI')
        sleep(2)