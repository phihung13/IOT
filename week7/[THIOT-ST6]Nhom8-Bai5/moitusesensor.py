#!/usr/bin/env python

import time
from mraa import getGpioLookup
from gpiozero import LED

from grove.grove_moisture_sensor import GroveMoistureSensor
from grove.display.jhd1802 import JHD1802


lcd = JHD1802()
sensor = GroveMoistureSensor(0)
relay = LED(5)
    
while True:
        mois = sensor.moisture
        if mois == 0:
            relay.off()
        else:
            relay.on()
        print('moisture: {}'.format(mois))
        time.sleep(1)