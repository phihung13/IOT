import socket
import struct
from urllib import request, parse
server_ip = '0.0.0.0'
server_port = 20000
total_humi = 0
total_temp = 0
count = 0
avg_humi = 0
avg_temp = 0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)
print(f"Đang lắng nghe kết nối trên cổng {server_port}...")
client_socket, client_address = server_socket.accept()
print(f"Kết nối từ {client_address[0]}:{client_address[1]} đã được thiết lập.")

def make_param_thingspeak(humidity, temperature): 
    params = parse.urlencode({'field1': temperature, 'field2': humidity}).encode() 
    return params
def thingspeak_post(params):
    api_key_write = "VH7RW35C0KBKR3S3" 
    req = request.Request('https://api.thingspeak.com/update', method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("X-THINGSPEAKAPIKEY", api_key_write)
    r = request.urlopen(req, data=params) 
    response_data = r.read()
    return response_data
def send_control_signal(signal_byte):
    control_signal = struct.pack('B', signal_byte)
    client_socket.send(control_signal)

received_handshake = client_socket.recv(1024).decode()
if received_handshake == "Up":
    handshake_message = "Handshake OK"
    client_socket.send(handshake_message.encode())
    received_ok = client_socket.recv(1024).decode()
    if received_ok == "OK":
        while True:
            data = client_socket.recv(1024)
            if len(data) >= 5:
                start_byte, id_byte, cmd_byte, length_byte, crc_byte = struct.unpack('BBBBB', data[:5])
                received_data = data[5:-1]
                stop_byte = data[-1]
                data_crc = sum(received_data) & 0xFF
                if (start_byte == 100) and (id_byte == 60) and (cmd_byte == 1) and (data_crc == crc_byte) and (stop_byte == 200):
                        temperature, humidity = struct.unpack('HH', received_data)
                        temp = temperature / 100.0
                        humi = humidity / 100.0

                        print(f"Nhiệt độ: {temp} °C")
                        print(f"Độ ẩm: {humi} %")
                        
                        total_humi +=humi
                        total_temp +=temp
                        count = count + 1
                        print(count)
                        if count in [1,2,6,7,11,12,16,17]:
                            print("Gửi tín hiệu Bật LED")
                            send_control_signal(0x01)
                        elif count in [3,4,5,8,9,10,13,14,15,18,19,20]:
                            print("Gửi tín hiệu Tắt LED")
                            send_control_signal(0x02)
                        if count == 20:
                            print("Gia tri trung binh")
                            avg_humi = total_humi/20
                            print(avg_humi)
                            avg_temp = total_temp/20
                            print(avg_temp)
                            total_humi = 0
                            total_temp = 0
                            count = 0
                            params_thingspeak = make_param_thingspeak(avg_humi,avg_temp) 
                            data = thingspeak_post(params_thingspeak)
                            print("Đã gửi lên thingspeak")
                else:
                    print("Lỗi CRC. Gói tin không hợp lệ.")
            else:
                print("Gói tin không đủ kích thước.")
