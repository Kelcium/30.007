import RPi.GPIO as GPIO
import time

def distance_check(TRIG, ECHO):
	print("Checking distance!")
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)

	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)

	start = time.time()
	end = time.time()

	while GPIO.input(ECHO) == 0:
		start = time.time()

	while GPIO.input(ECHO) == 1:
		end = time.time()

	duration = end - start
	dist = round(duration * 17150, 2)

	print("The measured distance is", dist, "!")
	return dist
	
dist = distance_check(23, 24)

while True and dist > 5:
	dist = distance_check(23, 24)
	time.sleep(0.5)
