#KHAO SAT SOUND SENSOR
from time import sleep
from grove.grove_sound_sensor import GroveSoundSensor
from grove.display.jhd1802 import JHD1802

sensor = GroveSoundSensor(2)
lcd = JHD1802()
while True:
    value = sensor.sound
    print("Gia tri dien ap cua sound sensor: {}".format(value))
    if value > 120:
        lcd.setCursor(0, 0)
        lcd.write('  HAY GIU')
        lcd.setCursor(1, 0)
        lcd.write('  IM LANG')
    else:
        lcd.setCursor(0, 0)
        lcd.write('  .......')
        lcd.setCursor(1, 0)
        lcd.write(' ........')
    sleep(2)
    

