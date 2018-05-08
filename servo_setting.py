import RPi.GPIO as GPIO
import time
servo1_pin = 23
servo2_pin = 24
def init():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servo1_pin,GPIO.OUT)
    GPIO.setup(servo2_pin,GPIO.OUT)
    pwm1 = GPIO.PWM(servo1_pin,50)
    pwm2 = GPIO.PWM(servo2_pin,50)
    return pwm1,pwm2
def setServo(servo1,servo2):
    pwm1,pwm2 = init()
    pwm1.start(7)
    pwm2.start(7)
    DC1 = 1./18.*(servo1)+2
    DC2 = 1./18.*(servo2)+2
    pwm1.ChangeDutyCycle(DC1)
    pwm2.ChangeDutyCycle(DC2)
    time.sleep(2)
#DC = 1./18.*(180)+2
#pwm.ChangeDutyCycle(DC)
    pwm1.stop()
    pwm2.stop()
    #GPIO.cleanup()