#!/usr/bin/python
import serial
import time
import os
import matplotlib.pyplot as plt
import threading
import numpy

ser = serial.Serial('/dev/ttyAMA0',  115200, timeout = 0)	#Open the serial Port
ser.flushInput()	# Clear the input buffer

def receive():
  ser.write('s')
  cond = True
  num=[]
  while cond:
    c = ser.read()
    if c=='\n':
      cond = False
    elif c=='A':
      line=0;
    elif len(c):
      num.append(c)
  numstr=''.join(num)
  return int(numstr)

#Recieve a line from the Arduberry and return it back
def get_data():
  global data
  data = [0]
  while True:
      data.append(receive())

	
try:
  while True:
    #put data reader in a thread so it can run simultaneous
    thread1 = threading.Thread(target=get_data)
    thread1.daemon = True
    thread1.start()
    
    #setup plt and make interactive
    plt.ion()
    fig=plt.figure()
    datalen=len(data)-1
    ln = plt.plot(range(datalen),data[0:datalen],'r-')[0]
    plt.show()
    #keep plotting
    while True:
      datalen=len(data)-1
      ln.set_xdata(range(datalen))
      ln.set_ydata(data[0:datalen])
      plt.axis([datalen-1500,datalen-1,100,500])
      fig.canvas.draw()
except KeyboardInterrupt:	#If program is terminated, close the serial port before exiting
  ser.close()