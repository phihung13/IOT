from time import sleep
from grove.grove_touch_sensor import GroveTouchSensor
from gpiozero import LED

relay=LED(5)
touch=GroveTouchSensor(12)

def cham(i):
    relay.on()
def tha(i):
    relay.off()

touch.on_press=cham
touch.on_release=tha
sleep(1)
