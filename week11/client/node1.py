import paho.mqtt.client as mqtt
from time import sleep
from random import randint
import json
from datetime import datetime
import threading
# from seeed_dht import DHT
# from gpiozero import LED
import socket
import ast


"""
Khởi tạo các giá trị cần thiết cho Master NODE
"""

"""Khởi các thông số cho Client kết nối với EMQX Broker để gửi và nhận dữ liệu"""
device_name = "NODE1"
username="node1"
password ="1"
client_id = "node1"
IP_SERVER = "127.0.0.1"
port = 1883


# Topic node public data
top_temp = "temp"
top_humi = "humi"
top_sonic = "sonic"
top_light = "light"
top_thump = "thump"

# Topic node subcribe
top_led1 = "led1"
top_led2 = "led2"
top_ledstick = "ledstick"
top_digit = "digit"
top_lcd = "lcd"



# Khai báo các cảm biến và cơ cấu chấp hành
# led1 = LED(5)
# led2 = LED(6)
# led_stick = 
# digit = 
lcd_1 = ""

# SENSOR = DHT('11', 18)
# sonic =
# light =   
thump = 0


"""Khai báo IP, PORT và kích bước vùng đệm cho UDP Master NODE dùng để giao tiếp với UDP Slaver"""
localIP = "0.0.0.0"
localPort = 11000
bufferSize = 1024

# Khởi tạo socket cho UDP Master và lắng nghe kết nối
UDP_Server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDP_Server.bind((localIP, localPort))
print("UDP server up and listening")

"""Định nghĩa các hàm chức năng cho EMQX Client"""
# Hàm connect kết nối tới EMQX Broker và subcribe các topic điều khiển actuator
def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code {}".format(rc))
    client.subscribe(top_led1)
    client.subscribe(top_led2)
    client.subscribe(top_ledstick)
    client.subscribe(top_digit)
    client.subscribe(top_lcd)

# Hàm disconnect ngắt kết nối với EMQX Broker
def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")

# Hàm gửi dữ liệu nhiệt độ cho topic nhiệt độ
def pub_temp(device_name: str, temp: int):
    data = {
        "device_name": device_name,
        "temp": temp,
    }
    payload = json.dumps(data)
    print("TEMP: ", payload)
    client.publish(topic=top_temp, payload= payload, retain=True)

# Hàm gửi dữ liệu độ ẩm
def pub_humi(device_name: str, humi: int):
    data = {
        "device_name": device_name,
        "humi": humi,
    }
    payload = json.dumps(data)
    print("HUMI: ", payload)
    client.publish(topic=top_humi, payload= payload, retain=True)

# Hàm gửi dữ liệu khoảng cách
def pub_sonic(device_name: str, sonic: int):
    data = {
        "device_name": device_name,
        "sonic": sonic,
    }
    payload = json.dumps(data)
    print("sonic: ", payload)
    client.publish(topic=top_sonic, payload= payload, retain=True)

# Hàm gửi dữ liệu ánh sáng
def pub_light(device_name: str, light: int):
    data = {
        "device_name": device_name,
        "light": light,
    }
    payload = json.dumps(data)
    print("light: ", payload)
    client.publish(topic=top_light, payload= payload, retain=True)

# Hàm gửi dữ liệu thump
def pub_thump(device_name: str, thump: int):
    data = {
        "device_name": device_name,
        "thump": thump,
    }
    payload = json.dumps(data)
    print("thump: ", payload)
    print("")
    client.publish(topic=top_thump, payload= payload, retain=True)

""" Hàm nhận tin nhắn từ EMQX Broker và kiểm tra tin nhắn thuộc topic nào để điều khiển actuator tương ứng"""
def on_message(client, userdata, msg):
    global lcd_1
    if msg.topic == top_led1:
        led1 = msg.payload.decode()
        led1 = json.loads(led1)
        print("Topic LED1: {}\n".format(led1))
        if led1["led1"] == True:
            # led1.on()
            print("LED1 ON")
        else:
            # led1.off()
            print("LED1 OFF")
        
    if msg.topic == top_led2:
        led2 = msg.payload.decode()
        led2 = json.loads(led2)
        print("Topic LED2: {}\n".format(led2))
        if led2["led2"] == True:
            # led2.on()
            print("LED2 ON")
        else:
            # led2.off()
            print("LED2 OFF")

    if msg.topic == top_ledstick:
        ledstick = msg.payload.decode()
        ledstick = led2 = json.loads(ledstick)
        print(ledstick["ledstick"])
        print("Topic LED Stick: {}\n".format(ledstick))

    if msg.topic == top_digit:
        digit = msg.payload.decode()
        digit = json.loads(digit)
        print(digit["digit"])
        print("Topic DIGIT: {}\n".format(digit))

    if msg.topic == top_lcd:
        lcd_1 = msg.payload.decode()
        lcd_1 = ast.literal_eval(lcd_1)
        lcd_1 = lcd_1["lcd"]
        print("Topic LCD: {}\n".format(lcd_1))

"""Định nghĩa các hàm chức năng cho UDP Master NODE"""
# Xử lí dữ liệu nhận được từ slaver
def processReceived(dataReceived):
    input_string = dataReceived.decode("utf-8")
    data_dict = ast.literal_eval(input_string)
    return data_dict

# Tạo và đóng gói frame dữ liệu
def framePacking(start, id, cmd, data, stop):
    data_dict = {
        "Start": start,
        "ID": id,
        "CMD": cmd,
        "Length": len(data),
        "Data": data,
        "CRC": checksum(start, id, cmd, len(data), data, stop),
        "Stop": stop
    }
    return data_dict

# Tính tổng độ dài dữ liệu 1 frame truyền
def checksum(start, id, cmd, length, datasets, stop):
    checksum = 0
    checksum +=(start+id+cmd+length+len(datasets)+stop)
    return checksum

# Kiểm tra gói tin
def checkCRC(crc1, crc2):
    if crc1 == crc2:
        return True
    else:
        return False


"""Khởi tạo EMQX Client và ghi đè các hàm chức năng, kết nối tới Broker và chạy chương trình trong luồng chính để lắng nghe tin nhắn từ Broker"""
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set(username=username, password= password)
client.connect(IP_SERVER, port, 60)
client.loop_start()

"""Hàm thực thi đọc giá trị từ cảm biến và gửi dữ liệu đến Broker"""
def publish_data():
    while True:
        # humi, temp = SENSOR.read()
        humi= 50
        temp = 50
        pub_temp(device_name, temp)
        pub_humi(device_name,  humi)
        # pub_light(device_name,  light)
        # pub_sonic(device_name,  sonic)
        # pub_thump(device_name, thump)
        sleep(5)

"""Hàm giao tiếp với UDP Slaver"""
def comunicate_slaver():
    global thump
    while True:
    
        # Tạo frame dữ liệu truyền cho UDP slaver và chuyển đổi sang byte
        msgToClient = str(framePacking(0x01, 0x00, 0x02, [lcd_1], 0x00))
        bytesToSend = str.encode(msgToClient)

        # Nhận dữ liệu từ UDP slaver
        ClientMsg = UDP_Server.recvfrom(bufferSize)

        # Xử lí dữ liệu nhận được từ UDP slaver
        ClientMsg_message = ClientMsg[0]
        ClientMsg_address = ClientMsg[1]
        data_dict = processReceived(ClientMsg_message)

        message = "Mesage from Slaver: {}".format(data_dict)
        address = "Adress of Master: {}".format(ClientMsg_address)

        # IN ra màn hình dữ liệu nhận được từ Slaver và địa chị của Slaver
        print(data_dict)
        print(address)

        # Tính độ dài frame dữ liệu
        crc2 = checksum(data_dict['Start'], data_dict['ID'], data_dict['CMD'], len(data_dict['Data']),data_dict['Data'], data_dict['Stop'])

        # Kiểm tra độ dài frame dữ liệu
        if(checkCRC(data_dict['CRC'],crc2)):

            address = "Client IP + Port: {}".format(ClientMsg_address)
            # Đọc giá trị cảm biến trong Frame dữ liệu 
            thump=data_dict['Data']
            print(data_dict['Data'])

            # Gửi frame dữ liệu về UDP slaver
        UDP_Server.sendto(bytesToSend, ClientMsg_address)
        print("===============================================\n")
        sleep(2)

# Tạo luồng mới thứ 2 cho thực thi hàm gửi dữ liệu
publish_thread = threading.Thread(target=publish_data)
publish_thread.start()

# Tạo luồng mới thứ 3 cho thực hàm giao tiếp với UDP Slaver
comunicate_thread = threading.Thread(target=comunicate_slaver)
comunicate_thread.start()