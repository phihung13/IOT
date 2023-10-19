import time
from rpi_ws281x import PixelStrip, Color

LED_COUNT = 10      
LED_PIN = 18        
LED_FREQ_HZ = 800000 
LED_DMA = 10        
LED_BRIGHTNESS = 255 
LED_INVERT = False  
LED_CHANNEL = 0 

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS,LED_CHANNEL)

strip.begin()
colors = [Color(255,0,0),Color(0,255,0),Color(0,0,255)]
while True:
    for color in colors:
        for i in range(LED_COUNT):
            strip.setPixelColor(i,color)
        time.sleep(1)
