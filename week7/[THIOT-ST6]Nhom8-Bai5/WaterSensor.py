from time import sleep
from grove.adc import ADC
from gpiozero import LED
from grove.display.jhd1802 import JHD1802
import time as tg
from datetime import datetime, time
lcd = JHD1802()
relay=LED(5)
sensor = ADC()

while True:
    b = tg.strftime("%H"+"h"+':'+"%M"+"m")
    current_time = datetime.now().time()
    value = sensor.read_voltage(0)
    if value < 1000:
        relay.on()
        lcd.setCursor(0, 0)
        lcd.write('Troi dang mua')
        lcd.setCursor(1,0)
        lcd.write('tg: '+b)
    else:
        lcd.setCursor(0, 0)
        lcd.write('Troi nang     ')
        lcd.setCursor(1,0)
        lcd.write('tg: '+b)
        relay.off()
    print(value)
    sleep(1)
