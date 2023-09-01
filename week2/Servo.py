import time

from grove.grove_servo import GroveServo

def main():
    servo =GroveServo(16)

    while True:
        Servo.setAngle(180)
        time.sleep(1)

        Servo.setAngle(0)
        time.sleep(1)

if __name__ == '__main__':
    main()