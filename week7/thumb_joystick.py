from grove.display.jhd1802 import JHD1802
from time import sleep
from grove.grove_thumb_joystick import GroveThumbJoystick

sensor = GroveThumbJoystick(0)
lcd = JHD1802()
while True:
    x,y = sensor.value
    print("gia tri truc hoanh X : ",x)
    print("gia tri truc tung Y : ",y)
    lcd.setCursor(0,0)
    lcd.write("Truc tung: {}".format(y))
    lcd.setCursor(1,0)
    lcd.write("Truc hoanh: {}".format(x))
    sleep(2)
