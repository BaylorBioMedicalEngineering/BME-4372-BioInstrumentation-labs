import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

device_folder=glob.glob('/sys/bus/w1/devices/28*')[0]
device_file=device_folder+'/w1_slave'

def read_w1_file():
  f=open(device_file,'r')
  lines=f.readlines()
  f.close()
  return lines

def read_temp():
  lines=read_w1_file()
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines=read_w1_file()
  temp_loc=lines[1].find('t=')
  if temp_loc != -1:
    temp_string=lines[1][temp_loc+2:]
    temp_c=float(temp_string)/1000.0
    temp_f=temp_c*9.0/5.0+32.0
    return temp_c, temp_f

while True:
  print(read_temp())
  time.sleep(1)
