import RPi.GPIO as GPIO
from time import sleep
from array import *
import time
import os

XlimitSwitch = 10
GPIO.setmode(GPIO.BCM)
GPIO.setup(XlimitSwitch,GPIO.IN)
YlimitSwitch = 9
GPIO.setmode(GPIO.BCM)
GPIO.setup(YlimitSwitch,GPIO.IN)
ZlimitSwitch = 11
GPIO.setmode(GPIO.BCM)
GPIO.setup(ZlimitSwitch,GPIO.IN)

prev_input_x = 1
prev_input_y = 1
prev_input_z = 1
while True:
  #take a reading
  inputX = GPIO.input(XlimitSwitch)
  inputY = GPIO.input(YlimitSwitch)
  inputZ = GPIO.input(ZlimitSwitch)
  #print(inputX)
  #print(inputY)
  #print(inputZ)
  #if the last reading was low and this one high, print
  if (not inputX):
    print("         X limit Switch pressed")
  elif (not inputY):
    print("         Y limit Switch pressed")
  elif (not inputZ):
    print("         Z limit Switch pressed")
  else:
	  print("Nothing pressed")
	
  if (not inputX and not inputY):
	  os.system("killall python")
  #slight pause to debounce
  time.sleep(0.05)
GPIO.cleanup()
print('Cycling Completed')
