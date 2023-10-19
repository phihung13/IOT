from grove.adc import ADC

class GroveLoudnessSensor:

    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC() 

    @property
    def value(self):
        value = self.adc.read(self.channel)
        return value

sensor = GroveLoudnessSensor(6)

while True:
    print("Gia tri tieng on {}".format(sensor.value))
    time.sleep(2)
