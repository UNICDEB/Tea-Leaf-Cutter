import RPi.GPIO as GPIO
from time import sleep

# Direction pin from controller
DIR = 10
# Step pin from controller
STEP = 8
# 0/1 used to signify clockwise or counterclockwise.
CW = 1
CCW = 0
# Direction pin from controller
DIR1 = 13
# Step pin from controller
STEP1 = 11


# Setup pin layout on PI
GPIO.setmode(GPIO.BOARD)

# Establish Pins in software
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

# Setup pin layout on PI
GPIO.setmode(GPIO.BOARD)

# Establish Pins in software
GPIO.setup(DIR1, GPIO.OUT)
GPIO.setup(STEP1, GPIO.OUT)

try:
	# Run forever.
	while True:

		"""Change Direction: Changing direction requires time to switch. The
		time is dictated by the stepper motor and controller. """
		sleep(1.0)
		# Esablish the direction you want to go
		GPIO.output(DIR,CCW)
		GPIO.output(DIR1,CW)

		# Run for 200 steps. This will change based on how you set you controller
		for x in range(200):

			# Set one coil winding to high
			GPIO.output(STEP,GPIO.HIGH)
			# ~ GPIO.output(STEP1,GPIO.HIGH)
			# Allow it to get there.
			sleep(.0004) # Dictates how fast stepper motor will run
			# Set coil winding to low
			GPIO.output(STEP,GPIO.LOW)
			# ~ GPIO.output(STEP1,GPIO.LOW)
			sleep(.0004) # Dictates how fast stepper motor will run
		# Run for 200 steps. This will change based on how you set you controller
		
		sleep(0.5)
		for x in range(400):

			# Set one coil winding to high
			# ~ GPIO.output(STEP,GPIO.HIGH)
			GPIO.output(STEP1,GPIO.HIGH)
			# Allow it to get there.
			sleep(.0004) # Dictates how fast stepper motor will run
			# Set coil winding to low
			# ~ GPIO.output(STEP,GPIO.LOW)
			GPIO.output(STEP1,GPIO.LOW)
			sleep(.0004) # Dictates how fast stepper motor will run



# Once finished clean everything up
except KeyboardInterrupt:
	print("cleanup")
	GPIO.cleanup()
