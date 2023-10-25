#KHAO SAT ADC BIEN TRO
from time import sleep
from grove.adc import ADC
from gpiozero import PWMLED

sensor = ADC()
led = PWMLED(5)

while True:
    value = sensor.read_voltage(0)
    print("Gia tri diep ap bien tro: {}".format(value))
    if value == 0:
        led.value =0
    elif value > 0 and value < 2000:
        led.value = 0.5
    elif value > 2000:
        led.value = 1
    sleep(1)