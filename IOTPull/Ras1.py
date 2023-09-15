from urllib import request, parse
from time import sleep
from random import randint 
from datetime import datetime

def http(): 
    def make_param_thingspeak(humi,temp,random):
        params = parse.urlencode({'field1':humi,'field2':temp,'field3':random }).encode()
        return params

    def thingspeak_post(params):
        api_key_write = "FUW4OM4UGHI91T8C"
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
            rd = randint(0,100)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("do am",humi)
            print("nhiet do",temp)
            print("tin hieu random",rd)
            params_thingspeak = make_param_thingspeak(humi,temp,rd)
            thingspeak_post(params_thingspeak)
            sleep(20)
            
        except:
            print('KHONG CO INTERNET \n KIEM TRA VA THU LAI')
            sleep(2)
   
http()