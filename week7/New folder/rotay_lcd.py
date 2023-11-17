import time
from grove.adc import ADC
from gpiozero import LED

class GroveRotarySensor:

    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def value(self):
        value = self.adc.read(self.channel)
        return value

sensor = GroveRotarySensor(4)
led=LED(5)

while True:
    print("Góc quay {}".format(sensor.value))
    if((sensor.value)>500):
        led.on()
    else: 
        led.off()       
    time.sleep(2)
