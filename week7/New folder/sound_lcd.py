#KHAO SAT SOUND SENSOR
from time import sleep
from grove.grove_sound_sensor import GroveSoundSensor
from grove.display.jhd1802 import JHD1802

sensor = GroveSoundSensor(2)
lcd = JHD1802()
while True:
    value = sensor.sound
    print("sound sensor: {}".format(value))
    if value > 120:
        lcd.setCursor(0, 2)
        lcd.write('KEEP SILENT')
    else:
        lcd.setCursor(1, 3)
        lcd.write(' (=_=)')
    sleep(2)
    

