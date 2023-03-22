import RPi.GPIO as GPIO
import time

def distance_check():
	GPIO.setmode(GPIO.BCM)
	TRIG = 23
	GPIO.setup(TRIG, GPIO.OUT)
	ECHO = 24
	GPIO.setup(ECHO, GPIO.IN)
	
	present = False
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

	if dist < 8:
		return dist, True
	return dist, False


try:
	present = False
	while present == False:
		dist, present = distance_check()
		print ("Measured Distance = %.1f cm" % dist)
		if dist < 5:
			break
		time.sleep(1)

# 	 Reset by pressing CTRL + C
except KeyboardInterrupt:
	print("Measurement stopped by User")

GPIO.cleanup()
