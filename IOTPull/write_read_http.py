from urllib import request, parse
from time import sleep
import json
from grove.display.jhd1802 import JHD1802
from gpiozero import LED
from grove.grove_relay import GroveRelay

bz = LED(12)
lcd = JHD1802()
bz.off()
api_key_read = '4DZW3T92KGI107U9'
channel_ID = '2256373'
red = LED(5)
relay = GroveRelay(16)

def thingspeak_get_1():
    url = 'https://api.thingspeak.com/channels/%s/fields/1/last.json?api_key=%s'%(channel_ID,api_key_read)
    req = request.Request(url,method = 'GET')
    r = request.urlopen(req)
    respone_data = r.read().decode()
    respone_data = json.loads(respone_data)
    value = respone_data['field1']    
    return value
def thingspeak_get_2():
    url = 'https://api.thingspeak.com/channels/%s/fields/2/last.json?api_key=%s'%(channel_ID,api_key_read)
    req = request.Request(url,method = 'GET')
    r = request.urlopen(req)
    respone_data = r.read().decode()
    respone_data = json.loads(respone_data)
    value = respone_data['field2']    
    return value
def thingspeak_get_3():
    url = 'https://api.thingspeak.com/channels/%s/fields/3/last.json?api_key=%s'%(channel_ID,api_key_read)
    req = request.Request(url,method = 'GET')
    r = request.urlopen(req)
    respone_data = r.read().decode()
    respone_data = json.loads(respone_data)
    value = respone_data['field3']    
    return value

while True:
    value1 = thingspeak_get_1()
    value2 = thingspeak_get_2()
    value3 = thingspeak_get_3()
    print("do am ",value1)
    print('nhiet do',value2)
    print('random ',value3)
    lcd.setCursor(0, 0)
    lcd.write('t:{0:2}%'.format(value1))
    lcd.setCursor(0, 7)
    lcd.write('d:{0:2}*C'.format(value2))
    lcd.setCursor(1 , 0)
    lcd.write('rd:{0:2}'.format(value3))
    if int(value3) > 50:
        red.on()
    if int(value3) < 50:
        red.off()
    if int(value1) > 90:
        relay.on()
    if int(value1) < 80:
        relay.off()
    if int(value2) > 37:
        bz.on()
    if int(value2) < 31:
        bz.off()
    sleep(20)