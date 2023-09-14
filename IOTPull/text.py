from urllib import request, parse
from time import sleep
import json


api_key_read = '5Z2BYMR3LO3FHSW0'
channel_ID = '2271054'

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
    if int(value3) > 50:
        print("f1")
    if int(value3) < 50:
        print("f2")
    if int(value1) > 90:
        print("f3")
    if int(value1) < 80:
        print("f4")
    if int(value2) > 37:
        print("f5")
    if int(value2) < 31:
        print("f6")
    sleep(20)