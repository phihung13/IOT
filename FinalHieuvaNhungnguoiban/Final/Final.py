import json
from urllib import request, parse
from time import sleep
from gpiozero import LED
import Adafruit_DHT
import socket
import struct
from urllib import request, parse

server_ip = '0.0.0.0'
server_port = 20000
count = 0
led1 = LED(20)
led2 = LED(2)
sensor = Adafruit_DHT.DHT11
led1.off()
led2.off()




def make_param_thingspeak(temp, humi):
    params = parse.urlencode({'field5': temp, 'field4': humi}).encode()
    return params

def make_param_thingspeak1(humidity, temperature): 
    params1 = parse.urlencode({'field7': temperature, 'field6': humidity}).encode() 
    return params1

def thingspeak_post(params):
    api_key_write = "BWXKPCXW1JXZ8F63"
    req = request.Request('http://api.thingspeak.com/update',method="POST")
    req.add_header("Content-Type","application/x-www-form-urlencoded")
    req.add_header("X-THINGSPEAKAPIKEY",api_key_write)
    request.urlopen(req, data=params)

def send_control_signal(signal_byte):
    control_signal = struct.pack('B', signal_byte)
    client_socket.send(control_signal)



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
    humi, temp = Adafruit_DHT.read_retry(sensor,3)
    params_thingspeak = make_param_thingspeak(temp, humi)
    thingspeak_post(params_thingspeak)
    print('nhiet do = {}C va do am = {}%'.format(temp, humi))
            
            
            ###Control Led 1
    if status[1] == '1':
        led1.on()
        print("LED 1 on")
    elif status[1] == '0':
        led1.off()
            
    ###Control Led 2
    if status[0] == '1':
        led2.on()
        print("LED 2 on")
    elif status[0] == '0':
        led2.off()
            
    ###Gui tin hieu dieu khi
    if status[2] == '1':
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_ip, server_port))
        server_socket.listen(1)
        print(f"Đang lắng nghe kết nối trên cổng {server_port}...")
        client_socket, client_address = server_socket.accept()
        print(f"Kết nối từ {client_address[0]}:{client_address[1]} đã được thiết lập.")
        received_handshake = client_socket.recv(1024).decode()
        if received_handshake == "Up":
            handshake_message = "Handshake OK"
            client_socket.send(handshake_message.encode())
            received_ok = client_socket.recv(1024).decode()
            if received_ok == "OK":
                while 1:
                    print("Gửi tín hiệu điều khiển")
                    data = client_socket.recv(1024)
                    if len(data) >= 5:
                        start_byte, id_byte, cmd_byte, length_byte, crc_byte = struct.unpack('BBBBB', data[:5])
                        received_data = data[5:-1]
                        stop_byte = data[-1]
                        data_crc = sum(received_data) & 0xFF
                        if (start_byte == 100) and (id_byte == 60) and (cmd_byte == 1) and (data_crc == crc_byte) and (stop_byte == 200):
                            temp, humi = struct.unpack('HH', received_data)
                            temp = temp / 100.0
                            humi = humi / 100.0
                            print(f"Nhiệt độ: {temp} °C")
                            print(f"Độ ẩm: {humi} %")
                            count = count + 1
                            params_thingspeak1 = make_param_thingspeak1(humi,temp) 
                            data = thingspeak_post(params_thingspeak1)
                            if count in [0,2,4,6,8]:
                                print("Gửi tín hiệu Bật LED")
                                send_control_signal(0x01)
                            elif count in [1,3,5,7,9]:
                                print("Gửi tín hiệu Tắt LED")
                                send_control_signal(0x02)
                            if count == 10:
                                break            
    elif status[2] == '0':
        print("Lỗi CRC. Gói tin không hợp lệ.")
    sleep(1)        
    
           