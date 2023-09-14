from urllib import request, parse
from time import sleep
from seeed_dht import DHT 
import random
# Khởi tạo thiết bị
sensor = DHT('11', 5)

# Hàm tạo tham số cho Thingspeak
def make_param_thingspeak(humidity, temperature, random): 
    params = parse.urlencode({'field1': temperature, 'field2': humidity, 'field3': random}).encode() 
    return params

# Hàm gửi dữ liệu lên Thingspeak
def thingspeak_post(params):
    api_key_write = "GLU1HGTBFZEPJPKQ" 
    req = request.Request('https://api.thingspeak.com/update', method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("X-THINGSPEAKAPIKEY", api_key_write)
    
    r = request.urlopen(req, data=params) 
    response_data = r.read()
    return response_data 

# Vòng lặp chính
while True: 
    try:
        humidity, temperature = sensor.read() 
        num_random = random.randint(0, 100)
        print('Temperature {}C, Humidity {}%'.format(temperature, humidity))
        print(num_random)

        params_thingspeak = make_param_thingspeak(humidity, temperature, num_random) 
        data = thingspeak_post(params_thingspeak) 
        sleep(20) 
    except:
        print('Không có kết nối INTERNET') 
        sleep(2)