from gpiozero import Button, LED
from signal import pause

touch_pin = 26  
led_pin = 24   

touch_sensor = Button(touch_pin)
led = LED(led_pin)

def touch_pressed():
    led.on()

def touch_released():
    led.off()

touch_sensor.when_pressed = touch_pressed
touch_sensor.when_released = touch_released

pause()
