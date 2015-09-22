#!/usr/bin/python
import serial
import time
import os
import matplotlib.pyplot as plt
import threading
import numpy

ser = serial.Serial('/dev/ttyAMA0',  57600, timeout = 0)	#Open the serial Port
ser.flushInput()	# Clear the input buffer

#Recieve a line from the Arduberry and return it back
def get_data():
  global data
  data = [[0] for i in range(6)]
  for i in range(6):
    data[i][0]=0
  i=0
  while True:
    state = ser.readline()
    if len(state):
      data[i].append(state)
      i=i+1
    if i>5:
      i=0

	
while True:
  try:
    #put data reader in a thread so it can run simultaneous
    thread1 = threading.Thread(target=get_data)
    thread1.daemon = True
    thread1.start()
    
    #setup plt and make interactive
    plt.ion()
    fig=plt.figure()
    datalen=len(data[0])-1
    ln0 = plt.plot(range(datalen),data[0][0:datalen],'r-')[0]
    ln1 = plt.plot(range(datalen),data[1][0:datalen],'g-')[0]
    ln2 = plt.plot(range(datalen),data[2][0:datalen],'c-')[0]
    plt.show()
    #keep plotting
    while True:
      datalen=len(data[0])-1
      ln0.set_xdata(range(datalen))
      ln0.set_ydata(data[0][0:datalen])
      ln1.set_xdata(range(datalen))
      ln1.set_ydata(data[1][0:datalen])
      ln2.set_xdata(range(datalen))
      ln2.set_ydata(data[2][0:datalen])
      fig.canvas.draw()
      time.sleep(0.01)
  except KeyboardInterrupt:	#If program is terminated, close the serial port before exiting
    ser.close()