#!/usr/bin/python

import traceback
import math
#import rospy
import string
import serial

s = serial.Serial('/dev/razorimu', 57600)
#s.write('1 s.p\r\n')

g0 = 9.80665
grad2rad = 3.141592/180.0

tmpdata = ''
while True:
  line = s.readline()
  line = line.replace("$","")
  line = line.replace("#","")
  line = line.replace("\r","")
  line = line.replace("\n","")
  words = string.split(line,",")
  #print len(words)
  #tmpdata = tmpdata.strip('$')
  #tmpdata = tmpdata.strip('#')
  if len(words) > 2:
    try:
        accelx = float(words[0])*0.03646840148
        accely = float(words[1])*0.03646840148
        accelz = float(words[2])*0.03646840148
        gyrox = (float(words[3])/14.375)*0.0174532925
        gyroy = (float(words[4])/14.375)*0.0174532925
        gyroz = (float(words[5])/14.375)*0.0174532925
        magx = (float(words[6])*.00256)/10000
        magy = float(words[7])/230
        magz = float(words[8])/230
        #print magx

    except:
        print "Invalid line"
        #print ""
  #print tmpdata(1)
  #x = tmpdata.split(',')
  #print x
  #tmpdata = x[-1]
  #for data in x[:-1]:
  #  try:
  #      dollar,accelx,accely,accelz,gyrox,gyroy,gyroz,magx,magy,magz = map(float, data.split(','))
  #  except:
  #      traceback.print_exc()
  #      continue
    #print timestamp,magx,magy,magz,accelx,accely,accelz,gyrox,gyroy,gyroz,temperatureCoefficient
    #accelx *= g0/2048
    #accely *= g0/2048
    #accelz *= g0/2048
    #print math.sqrt(magx**2+magy**2+magz**2)
  #  print magx, magy, magz
