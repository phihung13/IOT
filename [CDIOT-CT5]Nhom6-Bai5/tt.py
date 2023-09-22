import paho.mqtt.client as mqtt
from time import sleep 
from grove.display.jhd1802 import JHD1802 
from seeed_dht import DHT 
from urllib import request, parse
import json
from gpiozero import LED
from datetime import datetime, time
import time as tg
from grove.grove_relay import GroveRelay

rl = GroveRelay(22)
lcd = JHD1802() 
start_time = time(18, 0)  # 18:00
end_time = time(22, 0)    # 22:00
red = LED(5)
bz = LED(18)
sensor = DHT('11',16)

led = 0
buzzer = 0
relay = 0

def make_param_thingspeak(humi,temp):
    params = parse.urlencode({'field5':humi,'field6':temp}).encode()
    return params

def thingspeak_post(params):
    api_key_write = "6TY1GM4LJODNQ7LD"
    req = request.Request('http://api.thingspeak.com/update',method="POST")
    req.add_header("Content-Type","application/x-www-form-urlencoded")
    req.add_header("X-THINGSPEAKAPIKEY",api_key_write)
    r = request.urlopen(req,data= params)
    respone_data = r.read()
    return respone_data
# đọc dữ liệu từ thingspeak
def thingspeak_get_data():
    api_key_read = "48AZQLO97YBSOS0T"
    channel_ID = "2268895"
    # Lấy dữ liệu từ field_num
    req = request.Request("https://api.thingspeak.com/channels/2268895/feeds.json?api_key=48AZQLO97YBSOS0T", method="GET")
    r = request.urlopen(req)
    response_data = r.read().decode()
    response_data = json.loads(response_data)
    # Dữ liệu lịch sử là một danh sách các mục
    data = response_data["feeds"]
    data_c = response_data["channel"]
    
while True:
    b = tg.strftime("%H"+"h"+':'+"%M"+"m")
    current_time = datetime.now().time()
    humi, temp = sensor.read()
    print(humi)
    print(temp)
    lcd.setCursor(0, 0)
    lcd.write('ND:{0:2}c'.format(temp))
    lcd.setCursor(0,7)
    lcd.write('DA:{0:5}%'.format(humi))
    lcd.setCursor(1,0)
    lcd.write('tg: '+b)
    params_thingspeak = make_param_thingspeak(humi,temp)
    thingspeak_post(params_thingspeak)

    data,data_c = thingspeak_get_data()
    try:
        led = data[len(data)-1]['field%s'%(2)]
        led  = int(led)
        print(0)
    except:
        led = led
        print(1)
    print("led: ", led)

    try:
        buzzer = data[len(data)-1]['field%s'%(3)]
        print(buzzer)
        buzzer = int(buzzer)
    except:
        buzzer = buzzer
    print("buzzer: ", buzzer)
    try:
        relay = data[len(data)-1]['field%s'%(4)]
        relay = int([relay])
    except:
        relay = relay
    print("relay: ", relay)
    try:
        a_m =data[len(data)-1]['field%s'%(1)]
        a_m = int(a_m)
    except:
        a_m = a_m
    print("a_m: ", a_m)
    if a_m == 1 :
        if led == 1:
            red.on()
        if led == 0:
            red.off()
        if buzzer == 1:
            print(buzzer)
            bz.on()
        if buzzer == 0:
            bz.off()
        if relay == 1:
            print(relay)
            rl.on()
        if relay == 0:
            rl.off()
            
    if a_m == 0:
        red.off()
        rl.off()
        bz.off()
        if start_time <= current_time <= end_time:
            red.on()
        else:
            red.off()
        if temp > 37:
            bz.on()
        if temp < 31:
            bz.off()
        if humi > 90:
            rl.on()
        if humi < 60:
            rl.off()
    sleep(1)