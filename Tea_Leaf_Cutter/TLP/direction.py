import RPi.GPIO as GPIO
from time import sleep
from array import *
import time
import os


GPIO.setmode(GPIO.BCM)
	# X AXIS 
DIRX = 15
PULX = 18
	# Y AXIS
DIRY = 3
PULY = 2
	# Z AXIS
DIRZ = 27
PULZ = 17
	# CLAMP STEPPER
DIRC = 24
PULC = 23
	# LIMIT SWITCHES
XlimitSwitch = 10
YlimitSwitch = 9
ZlimitSwitch = 11
	
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIRX, GPIO.OUT)
GPIO.setup(PULX, GPIO.OUT)
GPIO.setup(DIRY, GPIO.OUT)
GPIO.setup(PULY, GPIO.OUT)
GPIO.setup(DIRZ, GPIO.OUT)
GPIO.setup(PULZ, GPIO.OUT)
GPIO.setup(DIRC, GPIO.OUT)
GPIO.setup(PULC, GPIO.OUT)
	
GPIO.setup(XlimitSwitch,GPIO.IN)
GPIO.setup(YlimitSwitch,GPIO.IN)
GPIO.setup(ZlimitSwitch,GPIO.IN)


def getCoordinates():
	f = open("/home/eduquis/Desktop/Final TLM codes/coordinates.txt", "r")
	mylist = f.read().split(', ')
	intList = [eval(i) for i in mylist]
	f.close()
	return intList

def distanceXDir(currentPos, newPos):
	if (newPos > currentPos) :
		return 1
	elif (newPos < currentPos):
		return 0
	else:
		return -1
	
def distanceDir(currentPos, newPos):
	if (newPos > currentPos) :
		return 1
	elif (newPos < currentPos):
		return 0
	else:
		return -1

def distaneFunction(currentPos, newPos):
	if (newPos > currentPos) :
		return (newPos - currentPos)
	elif (newPos < currentPos):
		return (currentPos - newPos)
	else:
		return 0

def moveXYForward(distx, disty):
	temp = -1
	if distx > disty:
		dif = distx - disty
		temp = 0
	elif distx < disty:
		dif = disty - distx
		temp = 1
	GPIO.output(DIRX, GPIO.HIGH)
	GPIO.output(DIRY, GPIO.LOW)
	delay = 0.0004
	if temp == 0:
		dist = distx - dif
	else:
		dist = disty - dif
	
	dist = dist * 200
	for x in range(dist): 
		GPIO.output(PULX, GPIO.HIGH)
		GPIO.output(PULY, GPIO.HIGH)
		sleep(delay)
		GPIO.output(PULX, GPIO.LOW)
		GPIO.output(PULY, GPIO.LOW)
		sleep(delay)
		
	if temp == 0:
		moveXForward(dif)
	else:
		moveYForward(dif)
	sleep(.005) # pause for possible change direction
	return

def moveXYBackward(distx, disty):
	temp = -1
	if distx > disty:
		dif = distx - disty
		temp = 0
	elif distx < disty:
		dif = disty - distx
		temp = 1
	GPIO.output(DIRX, GPIO.LOW)
	GPIO.output(DIRY, GPIO.HIGH)
	if temp == 0:
		dist = distx - dif
	else:
		dist = disty - dif
	
	dist = dist * 200
	delay = 0.0004
	valx = 1
	valy = 1
	for x in range(dist):
		limx = GPIO.input(XlimitSwitch)
		limy = GPIO.input(YlimitSwitch)
		if limx: 
			GPIO.output(PULX, GPIO.HIGH)
		if limy:
			GPIO.output(PULY, GPIO.HIGH)
		sleep(delay)
		GPIO.output(PULX, GPIO.LOW)
		GPIO.output(PULY, GPIO.LOW)
		sleep(delay)	
	if temp == 0:
		moveXBackward(dif)
	else:
		moveYBackward(dif)
	sleep(.005) # pause for possible change direction
	return		

def moveXBackwardYForward(distx, disty):
	temp = -1
	if distx > disty:
		dif = distx - disty
		temp = 0
	elif distx < disty:
		dif = disty - distx
		temp = 1
	GPIO.output(DIRX, GPIO.LOW)
	GPIO.output(DIRY, GPIO.LOW)
	delay = 0.0004
	if temp == 0:
		dist = distx - dif
	else:
		dist = disty - dif
	
	dist = dist * 200
	for x in range(dist): 
		limx = GPIO.input(XlimitSwitch)
		if limx: 
			GPIO.output(PULX, GPIO.HIGH)
		GPIO.output(PULY, GPIO.HIGH)
		sleep(delay)
		GPIO.output(PULX, GPIO.LOW)
		GPIO.output(PULY, GPIO.LOW)
		sleep(delay)
		
	if temp == 0:
		moveXBackward(dif)
	else:
		moveYForward(dif)
	sleep(.005) # pause for possible change direction
	return

def moveXForwardYBackward(distx, disty):
	temp = -1
	if distx > disty:
		dif = distx - disty
		temp = 0
	elif distx < disty:
		dif = disty - distx
		temp = 1
	GPIO.output(DIRX, GPIO.HIGH)
	GPIO.output(DIRY, GPIO.HIGH)
	if temp == 0:
		dist = distx - dif
	else:
		dist = disty - dif
	
	dist = dist * 200
	delay = 0.0004
	valx = 1
	valy = 1
	for x in range(dist):
		limx = GPIO.input(XlimitSwitch)
		limy = GPIO.input(YlimitSwitch)
		GPIO.output(PULX, GPIO.HIGH)
		if limy:
			GPIO.output(PULY, GPIO.HIGH)
		sleep(delay)
		GPIO.output(PULX, GPIO.LOW)
		GPIO.output(PULY, GPIO.LOW)
		sleep(delay)	
	if temp == 0:
		moveXForward(dif)
	else:
		moveYBackward(dif)
	sleep(.005) # pause for possible change direction
	return

def moveXForward(dist):
	GPIO.output(DIRX, GPIO.HIGH)
	dist = dist * 200
	delay = 0.0004
	for x in range(dist): 
		GPIO.output(PULX, GPIO.HIGH)
		sleep(delay)
		GPIO.output(PULX, GPIO.LOW)
		sleep(delay)
	sleep(.5) # pause for possible change direction
	return
	
	
def moveXBackward(dist):
	GPIO.output(DIRX, GPIO.LOW)
	dist = dist * 200
	delay = 0.0004
	for x in range(dist):
		lim = GPIO.input(XlimitSwitch) 
		if not lim:
			break 
		GPIO.output(PULX, GPIO.HIGH)
		sleep(delay)
		GPIO.output(PULX, GPIO.LOW)
		sleep(delay)
	sleep(.005) # pause for possible change direction
	return

def moveYForward(dist):
	GPIO.output(DIRY, GPIO.LOW)
	dist = dist * 200
	delay = 0.0004
	for x in range(dist): 
		GPIO.output(PULY, GPIO.HIGH)
		sleep(delay)
		GPIO.output(PULY, GPIO.LOW)
		sleep(delay)
	sleep(.5) # pause for possible change direction
	return
	
	
def moveYBackward(dist):
	GPIO.output(DIRY, GPIO.HIGH)
	dist = dist * 200
	delay = 0.0004
	for x in range(dist):
		lim = GPIO.input(YlimitSwitch)
		if not lim:
			break 
		GPIO.output(PULY, GPIO.HIGH)
		sleep(delay)
		GPIO.output(PULY, GPIO.LOW)
		sleep(delay)
	sleep(.005) # pause for possible change direction
	return

def moveZUpward(dist):
	GPIO.output(DIRZ, GPIO.LOW)
	dist = dist * 200
	delay = 0.0004
	for x in range(dist): 
		lim = GPIO.input(ZlimitSwitch)
		if not lim:
			break 
		GPIO.output(PULZ, GPIO.HIGH)
		sleep(delay)
		GPIO.output(PULZ, GPIO.LOW)
		sleep(delay)
	sleep(.005) # pause for possible change direction
	return
	
def moveZDownward(dist):
	GPIO.output(DIRZ, GPIO.HIGH)
	dist = dist * 200
	delay = 0.0004
	for x in range(dist): 
		GPIO.output(PULZ, GPIO.HIGH)
		sleep(delay)
		GPIO.output(PULZ, GPIO.LOW)
		sleep(delay)
	sleep(.005) # pause for possible change direction
	return

def openClamp(dist = 50):
	GPIO.output(DIRC, GPIO.HIGH)
	delay = 0.005
	for x in range(dist): 
		GPIO.output(PULC, GPIO.HIGH)
		sleep(delay)
		GPIO.output(PULC, GPIO.LOW)
		sleep(delay)
	sleep(.5) # pause for possible change direction
	return
	
	
def closeClamp(dist = 50):
	GPIO.output(DIRC, GPIO.LOW)
	delay = 0.005
	for x in range(dist): 
		GPIO.output(PULC, GPIO.HIGH)
		sleep(delay)
		GPIO.output(PULC, GPIO.LOW)
		sleep(delay)
	sleep(.5) # pause for possible change direction
	return


def origin():
	GPIO.output(DIRX, GPIO.LOW)
	GPIO.output(DIRY, GPIO.LOW)
	GPIO.output(DIRZ, GPIO.LOW)
	delay = 0.0004
	valx = 1
	valy = 1
	valz = 1
	while True:
		inputZ = GPIO.input(ZlimitSwitch)
		if not inputZ:
			valz = 0
			break
		elif inputZ and valz:
			moveZUpward(50)		
		time.sleep(0.005)
		
	# MOVING X and Y TO 0
	while True:
		#take a reading
		inputX = GPIO.input(XlimitSwitch)
		inputY = GPIO.input(YlimitSwitch)
		if not inputX:
			valx = 0
		if not inputY:
			valy = 0
		if not valx and not valy:
			break
		elif valx and valy:
			moveXYBackward(50, 100)
		elif inputY and valy:
			moveYBackward(50)
		elif inputX and valx:
			moveXBackward(50)		
		time.sleep(0.005)
	
	if(not valx and not valy and not valz):
			return
				
	return


def dropToBelt():
	GPIO.output(DIRX, GPIO.LOW)
	GPIO.output(DIRZ, GPIO.HIGH)
	delay = 0.0004
	valx = 1
	valz = 1
	# MOVING Z TO 0
	while True:
		inputZ = GPIO.input(ZlimitSwitch)
		if not inputZ:
			valz = 0
			break
		elif inputZ and valz:
			moveZUpward(50)		
		time.sleep(0.005)
		
	# MOVING X TO 0
	while True:
		#take a reading
		inputX = GPIO.input(XlimitSwitch)
		if not inputX:
			valx = 0
			break
		elif inputX and valx:
			moveXBackward(50)		
		time.sleep(0.005)
		
	# MOVING Z DOWN TILL BELT
	moveZDownward(30)
	
	# CLAMP OPEN
	openClamp()
	sleep(0.5)
	# CLAMP CLOSE
	closeClamp()
	
	valz = 1
	# MOVING Z TO 0
	while True:
		inputZ = GPIO.input(ZlimitSwitch)
		if not inputZ:
			valz = 0
			break
		elif inputZ and valz:
			moveZUpward(50)		
		time.sleep(0.005)
		
	return
	
# PROGRAM RUNS FROM HERE


arr = getCoordinates()
cycleCount = 0
totalcycles = arr[0]
index = 1

origin()
posX = 0
posY = 0
posZ = 0

while cycleCount < totalcycles:
	
	# X AXIS
	xdis = distaneFunction(posX, arr[index])
	xdir = distanceXDir(posX, arr[index])
	print(xdir, xdis)
	index = index + 1
	# Y AXIS
	ydis = distaneFunction(posY, arr[index])
	ydir = distanceXDir(posY, arr[index])
	print(ydir, ydis)
	posY = arr[index]
	index = index + 1
	
	if xdir == ydir and xdir == 0:
		moveXYBackward(xdis, ydis)
	
	elif xdir == ydir and xdir == 1:
		moveXYForward(xdis, ydis)
	
	elif xdir == 0 and ydir == 1:
		moveXBackwardYForward(xdis, ydis)
	
	elif xdir == 1 and ydir == 0:
		moveXForwardYBackward(xdis, ydis)
			
	# CLAMP OPEN
	openClamp()
		
	# Z AXIS
	zdis = distaneFunction(posZ, arr[index])
	zdir = distanceDir(posZ, arr[index])
	index = index + 1
	print(zdir, zdis)
	if zdir == 1:
		moveZDownward(zdis)
	else:
		moveZUpward(zdis)
		
	# CLAMP CLOSE
	closeClamp()
	
	# DROP TO BELT
	dropToBelt()
	
	posX = 0
	posZ = 0
	
	cycleCount = cycleCount + 1


	
GPIO.cleanup()

