import RPi.GPIO as GPIO
import time

vibration_pin = 24
motor_pin = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(vibration_pin, GPIO.IN)
GPIO.setup(motor_pin, GPIO.OUT)

while True:
    vibration_value = GPIO.input(vibration_pin)
    print("Giá trị cảm biến rung:", vibration_value)
    if vibration_value == GPIO.HIGH:
        print("có rung! Bật motor.")
        GPIO.output(motor_pin, GPIO.HIGH)
    else:
        print("Không có rung. Tắt motor.")
        GPIO.output(motor_pin, GPIO.LOW)
    time.sleep(0.1)
