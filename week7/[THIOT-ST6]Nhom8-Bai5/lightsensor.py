#
import time
from gpiozero import LED

from grove.grove_light_sensor_v1_2 import GroveLightSensor

sensor = GroveLightSensor(0)
red = LED(12)

while True:
    value = sensor.light
    print('Gia tri dien ap cam bien quang: {}'.format(value))
    if value < 500:
        red.on()
    else:
        red.off()  
    time.sleep(2)
