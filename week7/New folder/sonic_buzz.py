# ULTRASONIC ON OFF LED
import time
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from gpiozero import LED

red = LED(12)

sensor = GroveUltrasonicRanger(5)
    
while True:
    distance = sensor.get_distance()
    print('{} cm'.format(distance))
    if distance <= 50:
        red.on()
    else:
        red.off()
    time.sleep(1)