#!/usr/bin/python

import spidev
import time
import os
import matplotlib.pyplot as plt
import threading
import numpy
import RPi.GPIO as GPIO
PLTRANGE=400
WINDOW=40

spi = spidev.SpiDev()
spi.open(0,0)

IRPin = 23
RedPin = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RedPin, GPIO.OUT)
GPIO.output(RedPin, GPIO.LOW)
GPIO.setup(IRPin, GPIO.OUT)
GPIO.output(IRPin, GPIO.LOW)


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

# volts is from a 10 bit (2^10-1=1023)
# note 10 bits is approx 3 decimal places
def ConvertVolts(din):
  volts = round((din * 3.3) / float(1023),3)
  return volts


Hz=400
delay = 1.0/float(Hz)
led_delay=1.0/float(Hz)

# get red
def get_red():
  GPIO.output(RedPin, GPIO.HIGH)
  GPIO.output(IRPin, GPIO.LOW)
  time.sleep(led_delay)
  redval=ConvertVolts(ReadMCP3008(0))
  time.sleep(led_delay)
  return redval


# get ir
def get_ir():
  GPIO.output(IRPin, GPIO.HIGH)
  GPIO.output(RedPin, GPIO.LOW)
  time.sleep(led_delay)
  irval=ConvertVolts(ReadMCP3008(0))
  time.sleep(led_delay)
  return irval

# This just simulates reading from a socket.
def get_data():
  global data
  global datavg
  global redmm
  global irmm
  global ar
  data = [[0] for i in range(2)]
  data[0][0] = get_red()
  data[1][0] = get_ir()
  datavg = [[0] for i in range(2)]
  datavg[0][0] = data[0][0]
  datavg[1][0] = data[1][0]
  avgred=data[0][0]
  avgir=data[1][0]
  redmm = [[0] for i in range(2)]
  redmm[0][0] = data[0][0]
  redmm[1][0] = data[0][0]
  irmm = [[0] for i in range(2)]
  irmm[0][0] = data[1][0]
  irmm[1][0] = data[1][0]
  ar =[1]
  count=1
  while True:
    data[0].append(get_red())
    data[1].append(get_ir())
    count=count+1
    if count > WINDOW:
      avgred=avgred+data[0][count-1]-data[0][count-WINDOW]
      avgir=avgir+data[1][count-1]-data[1][count-WINDOW]
      datavg[0].append(avgred/WINDOW)
      datavg[1].append(avgir/WINDOW)
      redmm[0].append(min(data[0][count-WINDOW:count-1]))
      redmm[1].append(max(data[0][count-WINDOW:count-1]))
      irmm[0].append(min(data[1][count-WINDOW:count-1]))
      irmm[1].append(max(data[1][count-WINDOW:count-1]))
    else:
      avgred=avgred+data[0][count-1]
      avgir=avgir+data[1][count-1]
      datavg[0].append(data[0][count-1])
      datavg[1].append(data[1][count-1])
      redmm[0].append(min(data[0][0:count-1]))
      redmm[1].append(max(data[0][0:count-1]))
      irmm[0].append(min(data[1][0:count-1]))
      irmm[1].append(max(data[1][0:count-1]))
    ACred=redmm[1][count-1]-redmm[0][count-1]
    ACir=irmm[1][count-1]-irmm[0][count-1]
    if (ACir>0) & (datavg[0][count-1]>0):
      ar.append((ACred/datavg[0][count-1])*(datavg[1][count-1]/ACir))
    else:
      ar.append(ar[count-2])
    time.sleep(delay)

if __name__ == '__main__':
  try:
    #put data reader in a thread so it can run simultaneous
    thread1 = threading.Thread(target=get_data)
    thread1.daemon = True
    thread1.start()

    datavg=[[0] for i in range(2)]
    #setup plt and make interactive
    plt.ion()
    fig=plt.figure()
    datalen=len(data[0])-1
    ln0 = plt.plot(range(datalen),data[0][0:datalen],'r-')[0]
    ln1 = plt.plot(range(datalen),data[1][0:datalen],'g-')[0]
    ln2 = plt.plot(range(datalen),datavg[0][0:datalen],'r:')[0]
    ln3 = plt.plot(range(datalen),datavg[1][0:datalen],'g:')[0]
    ln4 = plt.plot(range(datalen),ar[0:datalen],'c-')[0]
    plt.axis([datalen-PLTRANGE,datalen-1,-0.1,3.6])
    plt.show()
    time.sleep(delay)
    #keep plotting
    while True:
      datalen=len(data[0])-1
      ln0.set_xdata(range(datalen))
      ln0.set_ydata(data[0][0:datalen])
      ln1.set_xdata(range(datalen))
      ln1.set_ydata(data[1][0:datalen])
      ln2.set_xdata(range(datalen))
      ln2.set_ydata(datavg[0][0:datalen])
      ln3.set_xdata(range(datalen))
      ln3.set_ydata(datavg[1][0:datalen])
      ln4.set_xdata(range(datalen))
      ln4.set_ydata(ar[0:datalen])
      plt.axis([datalen-PLTRANGE,datalen-1,-0.1,3.6])
      fig.canvas.draw()
      time.sleep(delay)
  except KeyboardInterrupt:
    f=open("output","w")
    datalen=len(data[0])-1
    f.write("Red\n")
    for ti in range(datalen):
      f.write(str(data[0][ti])+"\n")
    f.write("IR\n")
    for ti in range(datalen):
      f.write(str(data[1][ti])+"\n")
    f.close()
    spi.close()
    GPIO.cleanup()
    
    
    
    


