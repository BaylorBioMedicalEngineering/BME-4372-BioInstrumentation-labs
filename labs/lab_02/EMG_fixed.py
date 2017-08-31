#!/usr/bin/python
import serial
import time
import os
import matplotlib.pyplot as plt
import threading
import numpy
from struct import unpack

tmax=2000

ser = serial.Serial('/dev/ttyAMA0',  115200, timeout = 0)	#Open the serial Port
ser.flushInput()	# Clear the input buffer

data = [0 for i in range(tmax)]

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

for ti in range(tmax):
  print ti
  data[ti]=receive();

t=range(tmax)


fig=plt.figure()
plt.plot(t,data,'r-')
plt.show()

f=open("output","w")
for ti in range(tmax):
	f.write(str(data[ti])+"\n")
f.close()


try:
  while True:
    time.sleep(1)
except KeyboardInterrupt:
  ser.close()

