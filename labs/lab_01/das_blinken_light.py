# das_blinken_light.py

import RPi.GPIO as GPIO
import time

ledPin = 23

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, GPIO.LOW)

try:
  while True:
    GPIO.output(ledPin,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(ledPin,GPIO.LOW)
    time.sleep(1)
except KeyboardInterrupt:
  GPIO.cleanup()
