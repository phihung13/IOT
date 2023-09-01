from time import sleep
from gpiozero import LED

Listled = [[LED(17),LED(27)],
          [LED(4),LED(22)],
          [LED(3),LED(10)],
          [LED(2),LED(9)]]

while True:
     for i in Listled:
            i[0].on()
            i[1].on()
            sleep(1)
     for i in Listled:
            i[0].off()
            i[1].off()
     sleep(1)
