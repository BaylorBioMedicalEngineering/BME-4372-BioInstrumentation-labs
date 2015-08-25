# das_blinken_light_III.py

import RPi.GPIO as GPIO
import time

ledPin = 18
butPin = 22

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(butPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
pwm = GPIO.PWM(ledPin, 50)
pwm.start(100)

try:
  while True:
    if GPIO.input(butPin):
      pwm.ChangeDutyCycle(100)
    else:
      pwm.ChangeDutyCycle(25)
except KeyboardInterrupt:
  pwm.stop()
  GPIO.cleanup()
