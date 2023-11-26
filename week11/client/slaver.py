import socket
from time import sleep
import ast
import random

# Khởi tạo các cảm biến và cơ cấu chấp hành
# thump = ?
# lcd = ?

IP_SERVER = "192.168.1.24"


# Khai báo IP, PORT của UDP Master 
ServerAddressPort = (IP_SERVER, 11000)

# Khai báo kích thước vùng đệm của UDP slaver
bufferSize = 1024

# Xử lí dữ liệu nhận được từ slaver
def processReceived(dataReceived):
    input_string = dataReceived.decode("utf-8")
    data_dict = ast.literal_eval(input_string)
    return data_dict

# Tính tổng độ dài dữ liệu 1 frame truyền
def checksum(start, id, cmd, length, datasets, stop):
    checksum = 0
    checksum += (start + id + cmd + length + len(datasets) + stop)
    return checksum

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

i = 0
# Chương trình chính
while True:
    i += 1
    # Đọc giá trị từ cảm biến
    thump = 13
    # In giá trị cảm biến ra màn hình
    print("thump: ", thump)

    # Tạo frame dữ liệu truyền cho UDP Master và chuyển đổi sang byte
    msgToServer = str(framePacking(0x01, 0x01, 0x01, [thump], 0x00))
    bytesToSend = str.encode(msgToServer)

    # Khởi tạo socket và gửi dữ liệu cho UDP Master
    UDP_Client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDP_Client.sendto(bytesToSend, ServerAddressPort)

    try:
        # Nhận dữ liệu từ UDP Master
        ServerMsg = UDP_Client.recvfrom(bufferSize)
        ServerMsg_message = ServerMsg[0]
        ServerMsg_address = ServerMsg[1]

        message = "Message from Master: {}".format(ServerMsg_message)
        address = "Adress of Master: {}".format(ServerMsg_address)

        # IN ra màn hình dữ liệu nhận được từ master và địa chị của master
        print(message)
        print(address)

        # Xử lí dữ liệu nhận từ UDP Master
        mess = ServerMsg_message
        data = processReceived(mess)

        # Tính độ dài frame truyền dữ liệu
        crc2 = checksum(data['Start'], data['ID'], data['CMD'], len(data['Data']), data['Data'], data['Stop'])
        print("crc2: ", crc2)

        # Kiểm tra độ dài frame dữ liệu
        if (checkCRC(data['CRC'], crc2)):
            lcd_1 = data['Data'][0]

            # Kiểm tra tính hiệu hiển thị LCD nhận được từ Master
            print(lcd_1)
            
        print(f"Đã nhận được {i} dữ liệu từ Master.")

    except Exception as e:
        # In ra lỗi nếu không nhận được dữ liệu từ UDP Master
        print(e)
        
    print("===============================================\n")
    sleep(2)