import RPi.GPIO as GPIO
from time import sleep
from array import *
import time
import os

f = open("/home/eduquis/Desktop/TLP/coordinates.txt", "r")
mylist = f.read().split(', ')
print (mylist)
intList = [eval(i) for i in mylist]
print (intList)

counter = 0
print(intList[counter])
counter = counter + 1
print(intList[counter])
counter = counter + 1
print(intList[counter])

f.close()
