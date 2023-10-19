import socket
import struct
import time
from gpiozero import LED
from seeed_dht import DHT

led = LED(5)
sensor = DHT('11',12)
server_ip = '192.168.1.20'
server_port = 20000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

while True:
    client_socket.send(b'Up')
    received_handshake = client_socket.recv(1024).decode()
    if received_handshake == "Handshake OK":
        client_socket.send(b'OK')
        print("Bắt tay thành công!")
        while True:
            humidity, temperature = sensor.read()
            print('Temperature {}C, Humidity {}%'.format(temperature, humidity))

            if humidity is not None and temperature is not None:
                data = (int(temperature * 100), int(humidity * 100))
                data_byte = struct.pack('HH', *data)
                length_byte = len(data_byte)
                stop_byte = 200
                data_crc = sum(data_byte) & 0xFF

                packet = struct.pack('BBBBB', 100, 60, 1, length_byte, data_crc)
                packet += data_byte
                packet += struct.pack('B', stop_byte)
                client_socket.send(packet)
                time.sleep(1)
            data = client_socket.recv(1024)
            if len(data) >= 1:
                control_byte = data[0]
                if control_byte == 0x01:
                    print("Nhận được tín hiệu điều khiển: Bật LED")
                    led.on()
                elif control_byte == 0x02:
                    print("Nhận được tín hiệu điều khiển: Tắt LED")
                    led.off()
                else:
                    print("Tín hiệu điều khiển không hợp lệ.")
            else:
                print("Lỗi khi đọc dữ liệu từ cảm biến.")
    else:
        print("Lỗi trong quá trình bắt tay.")
        time.sleep(1)
