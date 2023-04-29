import RPi.GPIO as GPIO
from time import sleep
from array import *

# 0/1 used to signify clockwise or counterclockwise.
CW = 1
CCW = 0

# X AXIS (Direction pin from controller)
DIRX = 10
# Z AXIS (Step pin from controller)
STEPX = 8
# Y AXIS
DIRY = 5
STEPY = 3
# Z AXIS
DIRZ = 13
STEPZ = 11

# CLAMP STEPPER
DIRC = 18
STEPC = 16


# Setup pin layout on PI
GPIO.setmode(GPIO.BOARD)

# Establish Pins in software
GPIO.setup(DIRX, GPIO.OUT)
GPIO.setup(STEPX, GPIO.OUT)

# Establish Pins in software
GPIO.setup(DIRY, GPIO.OUT)
GPIO.setup(STEPY, GPIO.OUT)

# Establish Pins in software
GPIO.setup(DIRZ, GPIO.OUT)
GPIO.setup(STEPZ, GPIO.OUT)

# Establish Pins in software
GPIO.setup(DIRC, GPIO.OUT)
GPIO.setup(STEPC, GPIO.OUT)

a = array('i',[2,4000,120,7000,8000,7000,3000])
LIMX = 10000
LIMY = 8000
LIMZ = 8000



try:
	# Run forever.
	i = 0
	while (a[0]>0):

		"""Change Direction: Changing direction requires time to switch. The
		time is dictated by the stepper motor and controller. """
		sleep(1.0)
		# Esablish the direction you want to go
		
		GPIO.output(DIRX,CCW)
		GPIO.output(DIRY,CCW)
		GPIO.output(DIRZ,CW)
		# X AXIS
		i = i+1
		print (i)
		for x in range(a[i]):
			POSX = a[i]
			GPIO.output(STEPX,GPIO.HIGH)
			sleep(.0004) # Dictates how fast stepper motor will run
			# Set coil winding to low
			GPIO.output(STEPX,GPIO.LOW)
			sleep(.0004) # Dictates how fast stepper motor will run
		# Run for 200 steps. This will change based on how you set you controller
		
		sleep(0.05)
		
		# Y AXIS
		i=i+1
		for x in range(a[i]):
			GPIO.output(STEPY,GPIO.HIGH)
			sleep(.0004) # Dictates how fast stepper motor will run
			GPIO.output(STEPY,GPIO.LOW)
			sleep(.0004) # Dictates how fast stepper motor will run
		
		# For GRIPPER(TO OPEN)
		GPIO.output(DIRC,CW)
		for x in range(50):
			GPIO.output(STEPC,GPIO.HIGH)
			sleep(.005) # Dictates how fast stepper motor will run
			GPIO.output(STEPC,GPIO.LOW)
			sleep(.005) # Dictates how fast stepper motor will run
			
		# Z AXIS
		sleep(0.05)
		++i

		for x in range(a[i]):
			GPIO.output(DIRZ,CW)
			GPIO.output(STEPZ,GPIO.HIGH)
			sleep(.0001) # Dictates how fast stepper motor will run
			GPIO.output(STEPZ,GPIO.LOW)
			sleep(.0001) # Dictates how fast stepper motor will run
		
		# For GRIPPER(TO CLOSE)
		GPIO.output(DIRC,CCW)	
		for x in range(50):
			GPIO.output(STEPC,GPIO.HIGH)
			sleep(.005) # Dictates how fast stepper motor will run
			GPIO.output(STEPC,GPIO.LOW)
			sleep(.005) # Dictates how fast stepper motor will run
		
		GPIO.output(DIRZ,CCW)
		# Z AXIS RAISE GRIPPER	
		for x in range(LIMZ-a[i]):
			GPIO.output(STEPZ,GPIO.HIGH)
			sleep(.0004) # Dictates how fast stepper motor will run
			GPIO.output(STEPZ,GPIO.LOW)
			sleep(.0004) # Dictates how fast stepper motor will run
			
		# Y AXIS TO MOVE TO CONVEYOR BELT
		for x in range(LIMY-a[i-1]):
			GPIO.output(STEPY,GPIO.HIGH)
			sleep(.0004) # Dictates how fast stepper motor will run
			GPIO.output(STEPY,GPIO.LOW)
			sleep(.0004) # Dictates how fast stepper motor will run
		
		GPIO.output(DIRZ,CCW)
		# Z AXIS LOWER GRIPPER	
		for x in range(LIMZ-1000):
			GPIO.output(STEPZ,GPIO.HIGH)
			sleep(.0004) # Dictates how fast stepper motor will run
			GPIO.output(STEPZ,GPIO.LOW)
			sleep(.0004) # Dictates how fast stepper motor will run
		
		# For GRIPPER(TO DROP)
		GPIO.output(DIRC,CW)	
		for x in range(50):
			GPIO.output(STEPC,GPIO.HIGH)
			sleep(.009) # Dictates how fast stepper motor will run
			GPIO.output(STEPC,GPIO.LOW)
			sleep(.009) # Dictates how fast stepper motor will run
		
		GPIO.output(DIRZ,CCW)	
		# Z AXIS RAISE GRIPPER	
		for x in range(LIMZ):
			GPIO.output(STEPZ,GPIO.HIGH)
			sleep(.0004) # Dictates how fast stepper motor will run
			GPIO.output(STEPZ,GPIO.LOW)
			sleep(.0004) # Dictates how fast stepper motor will run
			
		# Function will be called to alter values
		# RANDOM CALCULATION
		if( a[i+1] > POSX):
			a[i+1] = a[i+1] - POSX
			GPIO.output(DIRX,CW)
		else:
			a[i+1] = POSX - a[i+1]
			GPIO.output(DIRX,CCW)
		
		
		a[i+2] = a[i+2] - LIMY
		GPIO.output(DIRY,CCW)
		a[i+3] = a[i+3] - LIMZ
		GPIO.output(DIRZ,CW)
			
		a[0] -= 1


# Once finished clean everything up
except KeyboardInterrupt:
	print("cleanup")
	GPIO.cleanup()
