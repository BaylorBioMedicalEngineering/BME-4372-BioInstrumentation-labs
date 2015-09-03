#!/usr/bin/env python


import RPi.GPIO as GPIO, time, os

DEBUG = 1
GPIO.setmode(GPIO.BCM)


def readadc(adcnum, clockpin, mosipin, misopin, cspin):
  if ((adcnum > 7) or (adcnum < 0)):
    return -1
  GPIO.output(cspin, True)
  GPIO.output(clockpin, False)  # start clock low
  GPIO.output(cspin, False)     # bring CS low

  commandout = adcnum
  commandout |= 0x18  # start bit + single-ended bit
  commandout <<= 3    # we only need to send 5 bits here
  for i in range(5):
    if (commandout & 0x80):
      GPIO.output(mosipin, True)
    else:
      GPIO.output(mosipin, False)
      commandout <<= 1
      GPIO.output(clockpin, True)
      GPIO.output(clockpin, False)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
      GPIO.output(clockpin, True)
      GPIO.output(clockpin, False)
      adcout <<= 1
      if (GPIO.input(misopin)):
      adcout |= 0x1

    GPIO.output(cspin, True)

    adcout /= 2       # first bit is 'null' so drop it
    return adcout
	
if __name__=='__main__':

	try:
		SPICLK = 18
		SPIMISO = 21
		SPIMOSI = 17
		SPICS = 22
		GPIO.setup(SPICLK, GPIO.OUT)
		GPIO.setup(SPIMISO, GPIO.IN)
		GPIO.setup(SPIMOSI, GPIO.OUT)
		GPIO.setup(SPICS, GPIO.OUT)

		print "| #0 \t #1 \t #2 \t #3 \t #4 \t #5 \t #6 \t #7\t|"
		print "-----------------------------------------------------------------"
		while True:
			print "|",
			for adcnum in range(8):
				ret = readadc(adcnum, SPICLK, SPIMOSI, SPIMISO, SPICS)
				print ret,"\t",
			print "|"

	except KeyboardInterrupt:
		pass

	GPIO.cleanup()
