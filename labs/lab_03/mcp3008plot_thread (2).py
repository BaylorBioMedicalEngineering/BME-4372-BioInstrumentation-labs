#!/usr/bin/python

import spidev
import time
import os
import matplotlib.pyplot as plt
import threading
import numpy
import RPi.GPIO as GPIO

pos_volt = 5.0
ref_gnd=2.5
neg_volt=0.0

SigPin = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SigPin, GPIO.OUT)
GPIO.output(SigPin,GPIO.LOW)

spi = spidev.SpiDev()
spi.open(0,0)

# send 1xxx0000 w/ xxx=channel(0-7)
# rec 3 bytes, 10 bit value is last part:
# xmit[0]  xmit[1]  xmit[2]
# xxxxxxxx xxxxxxA9 87654321
# xmit[1]&3 = 000000A9
# shift left 8 = 000000A900000000
# add xmit[2] =  000000A987654321
def ReadMCP3008(channel):
  xmit = spi.xfer2([1,(8+channel)<<4,0])
  cdata = ((xmit[1]&3) << 8) + xmit[2]
  return cdata

# volts is from a 10 bit (2^10-1=1023), Vref=3.3
# note 10 bits is approx 3 decimal places
def ConvertVolts(data):
  volts = round((data * (pos_volt-neg_volt)) / float(1023)-ref_gnd,3)
  return volts


Hz=1000
delay = 1.0/float(Hz)

SqHz=1
sqdelay = 2.0/float(Hz)

#class MyThread (threading.Thread)
# This just simulates reading from a socket.
def get_data():
  global data
  data = [[0] for i in range(8)]
  for i in range(8):
    data[i][0]=ConvertVolts(ReadMCP3008(i))
  while True:
    for i in range(8):
      data[i].append(ConvertVolts(ReadMCP3008(i)))
    time.sleep(delay)
    
def square_wave():
  while True:
    GPIO.output(SigPin,GPIO.HIGH)
    time.sleep(sqdelay)
    GPIO.output(SigPin,GPIO.LOW)
    time.sleep(sqdelay)

if __name__ == '__main__':
  try:
    #put data reader in a thread so it can run simultaneous
    thread1 = threading.Thread(target=get_data)
    thread1.daemon = True
    thread1.start()
    
    thread2 = threading.Thread(target=square_wave)
    thread2.daemon = True
    thread2.start()
    
    #setup plt and make interactive
    plt.ion()
    fig=plt.figure()
    datalen=len(data[0])
    ln0 = plt.plot(range(datalen),data[0][0:datalen],'r-')[0]
    ln1 = plt.plot(range(datalen),data[1][0:datalen],'g-')[0]
    ln2 = plt.plot(range(datalen),data[2][0:datalen],'c-')[0]
    plt.axis([0,datalen-1,neg_volt-ref_gnd-0.1,pos_volt-ref_gnd+0.1])
    plt.show()
    #keep plotting
    while True:
      datalen=len(data[0])
      ln0.set_xdata(range(datalen))
      ln0.set_ydata(data[0][0:datalen])
      ln1.set_xdata(range(datalen))
      ln1.set_ydata(data[1][0:datalen])
      ln2.set_xdata(range(datalen))
      ln2.set_ydata(data[2][0:datalen])
      plt.axis([0,datalen-1,neg_volt-ref_gnd-0.1,pos_volt-ref_gnd+0.1])
      fig.canvas.draw()
      time.sleep(delay)
  except KeyboardInterrupt:
    spi.close()
    GPIO.cleanup()
    
    
    
    


