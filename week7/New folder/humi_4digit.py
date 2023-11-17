#!/usr/bin/env python3

from datetime import datetime, time
from seeed_dht import DHT
from grove.display.jhd1802 import JHD1802
import time as tg

    # Grove - 16x2 LCD(White on Blue) connected to I2C port
lcd = JHD1802()

    # Grove - Temperature&Humidity Sensor connected to port D5
sensor = DHT('11', 5)

    
while True:
    b = tg.strftime("%H"+"h"+':'+"%M"+"m")
    current_time = datetime.now().time()
    humi, temp = sensor.read()
    print(humi)
    print(temp)
    lcd.setCursor(0, 0)
    lcd.write('ND:{0:2}c'.format(temp))
    lcd.setCursor(0,7)
    lcd.write('DA:{0:5}%'.format(humi))
    lcd.setCursor(1,0)
    lcd.write('tg: '+b)

import time
from grove.grove_4_digit_display import Grove4DigitDisplay

display = Grove4DigitDisplay(5,6)
count = 0
while True:
    t = time.strftime("%H%M",time.localtime(time.time()))
    display.show(t)
    
    display.set_colon(count&1)
    count+=1
    time.sleep(1)
