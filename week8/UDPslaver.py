import socket
from time import sleep
from seeed_dht import DHT
from gpiozero import LED
import ast
import random

# Khởi tạo các cảm biến
led = LED(22)
sensor = DHT("11", 5)

# Khai báo IP, PORT của UDP Master và tính hiệu điều khiển LED
ServerAddressPort = ("192.168.1.15", 11000)
control_signal = 0
# Khai báo kích thước vùng đệm của UDP slaver
bufferSize = 1024
i = -1

# Xử lí dữ liệu nhận được từ slaver
def processReceived(dataReceived):
    input_string = dataReceived.decode("utf-8")
    data_dict = ast.literal_eval(input_string)
    return data_dict

# Tính tổng độ dài dữ liệu 1 frame truyền
def checksum(start, id, cmd, length, datasets, stop):
    checksum = 0
    checksum += (start + id + cmd + length + sum(data for data in datasets) + stop)
    return (checksum * 2) + 6

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

# Kiểm tra gói tin
def checkCRC(crc1, crc2):
    if crc1 == crc2:
        return True
    else:
        return False

# Chương trình chính
while True:
    i += 1
    # Đọc giá trị từ cảm biến
    humi, temp = sensor.read()
    print("Tem: ", temp)
    print("HUMI: ", humi)

    # Tạo frame dữ liệu truyền cho UDP Master và chuyển đổi sang byte
    msgToServer = str(framePacking(0x01, 0x01, 0x01, [humi, temp], 0x00))
    bytesToSend = str.encode(msgToServer)

    # Khởi tạo socket và gửi dữ liệu cho UDP Master
    UDP_Client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDP_Client.sendto(bytesToSend, ServerAddressPort)

    # Nhận dữ liệu từ UDP Master
    try:
        ServerMsg = UDP_Client.recvfrom(bufferSize)
        ServerMsg_message = ServerMsg[0]
        ServerMsg_address = ServerMsg[1]

        message = "Message from Server: {}".format(ServerMsg_message)
        address = "Message from Server: {}".format(ServerMsg_address)

        # Xử lí dữ liệu nhận từ UDP Master
        a = ServerMsg_message
        data = processReceived(a)

        # Tính độ dài frame truyền dữ liệu
        crc2 = checksum(data['Start'], data['ID'], data['CMD'], len(data['Data']), data['Data'], data['Stop'])
        print("crc2", crc2)

        # Kiểm tra độ dài frame dữ liệu
        if (checkCRC(data['CRC'], crc2)):
            print(data)
            control_signal = data['Data'][0]
            # Kiểm tra tính hiệu điều điều khiển LED
            if control_signal == 1:
                led.on()
            else:
                led.off()

        print(message)
        print(address)
    except Exception as e:
        # In ra lỗi nếu không nhận được dữ liệu từ UDP Master
        print(e)
        
    print(i)
    print("===============================================")
    sleep(1)