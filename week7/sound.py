import time
from grove.adc import ADC

class GroveSoundSensor:

    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def value(self):
        value = self.adc.read(self.channel)
        return value

sensor = GroveSoundSensor(0)

while True:
    print("Gia tri tieng {}".format(sensor.value))
    time.sleep(2)
