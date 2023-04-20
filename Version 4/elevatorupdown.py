import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def elevator_move(test_dist, steps):
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	#PUL = 18  #temp
	PUL = 22 #true
	DIR = 27
	
	GPIO.setup(PUL, GPIO.OUT)
	GPIO.setup(DIR, GPIO.OUT)

	GPIO.output(DIR, GPIO.LOW)
	
	#distance = distance_check(23, 24)
	
	while test_dist > 5:
		for x in range(500):
			GPIO.output(PUL, GPIO.HIGH)
			time.sleep(0.0005)
			GPIO.output(PUL, GPIO.LOW)
			time.sleep(0.0005)
			steps += 1
			test_dist -= 0.1
		#distance = distance_check(23, 24)

	if test_dist < 5:
		GPIO.output(DIR, GPIO.HIGH)
		for x in range(100):
			GPIO.output(PUL, GPIO.HIGH)
			time.sleep(0.0005)
			GPIO.output(PUL, GPIO.LOW)
			time.sleep(0.0005)
			steps -= 1
	
	GPIO.cleanup()
	return steps

def elevator_full(steps):
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	PUL = 22 #true
	DIR = 27
	
	GPIO.setup(PUL, GPIO.OUT)
	GPIO.setup(DIR, GPIO.OUT)

	GPIO.output(DIR, GPIO.LOW)
	
	for x in range(9000 - steps):
		GPIO.output(PUL, GPIO.HIGH)
		time.sleep(0.0005)
		GPIO.output(PUL, GPIO.LOW)
		time.sleep(0.0005)
	
	GPIO.cleanup()
	
def elevator_return():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	PUL = 22
	DIR = 27
	
	GPIO.setup(PUL, GPIO.OUT)
	GPIO.setup(DIR, GPIO.OUT)

	GPIO.output(DIR, GPIO.HIGH)
	
	for x in range(9000):
		GPIO.output(PUL, GPIO.HIGH)
		time.sleep(0.0005)
		GPIO.output(PUL, GPIO.LOW)
		time.sleep(0.0005)
	
	GPIO.cleanup()

steps = 0
distance = 8

print("down")
distance -= 0.1
steps = elevator_move(distance, steps)

time.sleep(3)

elevator_full(steps)
time.sleep(3)

elevator_return()
