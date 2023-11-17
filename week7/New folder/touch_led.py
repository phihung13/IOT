from time import sleep
from grove.grove_touch_sensor import GroveTouchSensor
from gpiozero import LED

relay=LED(5)
touch=GroveTouchSensor(12)

def press(i):
    relay.on()
def release(i):
    relay.off()

touch.on_press=press
touch.on_release=release
sleep(1)
