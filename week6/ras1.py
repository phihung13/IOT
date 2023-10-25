from time import sleep
from datetime import datetime
import random
from urllib import request, parse
# from seeed_dht import DHT
import json

# SENSOR = DHT('11', 18)

API_KEY_READ = "I8P7YFO5L6S3USJT"
API_KEY_WRITE = "I0NZGALDUMZPNHIB"
CHANNEL_ID = "2317304"

# HANDLE PARAMETER TO POST TO SERVER
def make_param_thingspeak(humi,temp):
    params = parse.urlencode({'field4':temp,'field5':humi}).encode()
    return params

# POST DATA TO SERVER
def thingspeak_post(params):
    req = request.Request('http://api.thingspeak.com/update',method="POST")
    req.add_header("Content-Type","application/x-www-form-urlencoded")
    req.add_header("X-THINGSPEAKAPIKEY",API_KEY_WRITE)
    r = request.urlopen(req,data= params)
    respone_data = r.read()
    return respone_data

# MAIN LOOP
while True:
    try:        
        # GET DATA FROM SENSOR AFTER POST TO SERVER EACH 20S
        r_temp = random.randrange(0,100)
        r_humi = random.randrange(50,100)
        try:
            # humi, temp = SENSOR.read()
            # print("TEMP POST: ",temp)
            # print("HUMI POST: ",humi)
            pass
        except:
            print("KHONG THE DOC GIA TRI CAM BIEN")
        now = datetime.now()
        print("TEMP POST: ",r_temp)
        print("HUMI POST: ",r_humi)
        current_time = now.strftime("%H:%M:%S")
        print(current_time)
        params_thingspeak = make_param_thingspeak(r_humi,r_temp)
        if thingspeak_post(params_thingspeak):
            print("SUBMITTED SUCCESSFULLY")
    except:
        print('KHONG CO INTERNET \n KIEM TRA VA THU LAI')
    sleep(3)