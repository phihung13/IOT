#KHAO SAT THUMB JOYSTICK

from time import sleep
from grove.grove_thumb_joystick import GroveThumbJoystick
sensor = GroveThumbJoystick(0)
from gpiozero import LED
bz = LED(18)
red =LED(5)
while True:
    x,y = sensor.value
    print("gia tri truc hoanh X : ",x)
    print("gia tri truc tung Y : ",y)
    if y > 500:
        bz.on()
        red.off()
    elif y < 500:
        bz.off()
        red.on()
    sleep(1)
