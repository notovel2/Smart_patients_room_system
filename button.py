import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40,GPIO.IN)
while True:
    state = GPIO.input(40)
    print(state)
    time.sleep(0.1)