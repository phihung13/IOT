from time import sleep
from gpiozero import PWMLED

led_bar = PWMLED(17)

while True:
    led_bar.value=1
    sleep(1)
    led_bar.value=0
    sleep(1)
