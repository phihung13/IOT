from time import sleep
from grove.factory import Factory
from gpiozero import LED

red=LED(5)

while True:
    sensor = Factory.getTemper("NTC-ADC", 0)
    print('Detecting temperature...')
    while True:
        print('{} Celsius'.format(sensor.temperature))
        if sensor.temperature > 27:
            red.on()
        else:
            red.off()
        sleep(2)