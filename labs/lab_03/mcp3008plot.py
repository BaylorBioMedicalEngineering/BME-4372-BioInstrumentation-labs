#!/usr/bin/python

import spidev
import time
import os
import matplotlib.pyplot as plt
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
  cdata = ((xmit[1]&3) << 8) + xmit[2]
  return cdata

# volts is from a 10 bit (2^10-1=1023), Vref=3.3
# note 10 bits is approx 3 decimal places
def ConvertVolts(data):
  volts = round((data * 3.3) / float(1023),3)
  return volts


data = [[0] for i in range(8)]
for i in range(8):
  data[i][0]=ConvertVolts(ReadMCP3008(i))

Hz=1000
delay = 1.0/float(Hz)


def get_data():
    for i in range(8):
      data[i].append(ConvertVolts(ReadMCP3008(i)))


#if __name__ == '__main__':
try:
  get_data()
  get_data()
  #setup plt and make interactive
  plt.ion()
  fig=plt.figure()
  ln0 = plt.plot(range(len(data[0])),data[0],'r-')[0]
  ln1 = plt.plot(range(len(data[1])),data[1],'g-')[0]
  plt.axis([0,len(data[0])-1,-0.1,3.6])
  plt.show()
  #keep plotting
  while True:
    get_data()
    plt.pause(1)
    ln0.set_xdata(range(len(data[0])))
    ln0.set_ydata(data[0])
    ln1.set_xdata(range(len(data[1])))
    ln1.set_ydata(data[1])
    plt.axis([0,len(data[0])-1,-0.1,3.6])
    fig.canvas.draw()
    time.sleep(delay)
except KeyboardInterrupt:
  spi.close()
