#!/usr/bin/python
import serial
import time
import os
import matplotlib.pyplot as plt
import threading
import numpy
from struct import unpack


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

for ti in range(4):
  print ti
  line0=receive()
  print line0

  

ser.close()

