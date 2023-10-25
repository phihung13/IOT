import socket
import ast
import paho.mqtt.client as mqtt
from time import sleep

# khai báo IP, PORT và kích bước vùng đệm cho UDP master
localIP = "0.0.0.0"
localPort = 11000
bufferSize = 1024

# khai báo các giá trị cảm biến và led
humi = 0
temp = 0
i = -1
led = -1
led_status = 1

# Khởi tạo MQTT client
client = mqtt.Client("BCcLNBYqMyEOBz09IwYIKSY")
client.username_pw_set(username="BCcLNBYqMyEOBz09IwYIKSY", password="lejC9HJGwYHNi0LQ0aN4ALy/")

# Khởi tạo socket cho UDP Master và lắng nghe kết nối
UDP_Server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDP_Server.bind((localIP, localPort))
print("UDP server up and listening")

# Xử lí dữ liệu nhận được từ slaver
def processReceived(dataReceived):
    input_string = dataReceived.decode("utf-8")
    data_dict = ast.literal_eval(input_string)
    return data_dict

# Kết nối với MQTT Broker trên Thingspeak và gửi dữ liệu
def thingspeak_mqtt(data1, data2):
    client.connect("mqtt3.thingspeak.com", 1883, 60)
    channel_ID = "2313003"
    client.publish("channels/%s/publish" %(channel_ID),"field1=%s&field2=%s&status=MQTTPUBLISH" %(data1,data2))

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
    checksum +=(start+id+cmd+length+sum(data for data in datasets)+stop)
    return (2*checksum)+6

# Kiểm tra gói tin
def checkCRC(crc1, crc2):
    if crc1 == crc2:
        return True
    else:
        return False

# Chương trình chính
while True:
    i+=1
    led+=1
    if(led < 2):
        led_status = 1
    else:
        led_status = 0
    if(led == 4):
        led = -1

    # Tạo frame dữ liệu truyền cho UDP slaver và chuyển đổi sang byte
    msgToClient = str(framePacking(0x01, 0x00, 0x01, [led_status], 0x00))
    bytesToSend = str.encode(msgToClient)
    # Nhận dữ liệu từ UDP slaver
    ClientMsg = UDP_Server.recvfrom(bufferSize)

    # Xử lí dữ liệu nhận được từ UDP slaver
    ClientMsg_message = ClientMsg[0]
    ClientMsg_address = ClientMsg[1]
    data_dict = processReceived(ClientMsg_message)
    message = "Mesage from Client: {}".format(data_dict)

    # Tính độ dài frame dữ liệu
    crc2 = checksum(data_dict['Start'], data_dict['ID'], data_dict['CMD'], len(data_dict['Data']),data_dict['Data'], data_dict['Stop'])

    # Kiểm tra độ dài frame dữ liệu
    if(checkCRC(data_dict['CRC'],crc2)):
        address = "Client IP + Port: {}".format(ClientMsg_address)

        # Cộng dồn các giá trị nhận từ cảm biến
        humi+=data_dict['Data'][0]
        temp+=data_dict['Data'][1]

        # Kiểm tra số lượng dữ liệu nhận được và tính trung bình sau đó gửi lên MQTT Broker
        if i == 19:
            data2 = humi/20
            data1 = temp/20
            thingspeak_mqtt(data1, data2)
            humi = 0
            temp = 0
            i = -1
        print(data_dict)
        print(address)

        # Gửi frame dữ liệu về UDP slaver
    UDP_Server.sendto(bytesToSend, ClientMsg_address)
    print("===============================================")
    sleep(1)