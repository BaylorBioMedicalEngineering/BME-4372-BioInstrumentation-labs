#!/usr/bin/python

import spidev
import time
import os
import matplotlib.pyplot as plt
import threading
import numpy



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
  data = ((xmit[1]&3) << 8) + xmit[2]
  return data

# volts is from a 10 bit (2^10-1=1023), Vref=3.3
# note 10 bits is approx 3 decimal places
def ConvertVolts(data):
  volts = round((data * 3.3) / float(1023),3)
  return volts


#sample rate (approximate)
Hz=1000
delay = 1.0/float(Hz)


data = []

# This just simulates reading from a socket.
def data_listener():
  while True:
    for i in range(8):
      data[i].append(ConvertVolts(ReadMCP3008(i)))
    time.sleep(delay)

if __name__ == '__main__':
try:
  #put data reader in a thread so it can run simultaneous
  thread = threading.Thread(target=data_listener)
  thread.daemon = True
  thread.start()
  #setup plt and make interactive
  plt.figure()
  ln = plt.plot([])[0]
  plt.ion()
  plt.show()
  #keep plotting
  while True:
    plt.pause(1)
    ln.set_xdata(range(len(data)))
    ln.set_ydata(data[0])
    plt.draw()
except KeyboardInterrupt:
  spi.close()
