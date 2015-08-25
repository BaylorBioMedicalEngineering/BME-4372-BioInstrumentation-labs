# das_blinken_light_II.py

import RPi.GPIO as GPIO
import time

ledPin = 4
butPin = 22

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(butPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(ledPin, GPIO.LOW)

try:
  while True:
    GPIO.output(ledPin,GPIO.input(butPin))
    time.sleep(.1)
    GPIO.output(ledPin,GPIO.LOW)
    time.sleep(.1)
except KeyboardInterrupt:
  GPIO.cleanup()
