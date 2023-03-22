import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 23
GPIO.setup(TRIG, GPIO.OUT)

ECHO = 24
GPIO.setup(ECHO, GPIO.IN)

print("Distance measurement in progress")

present = False

def distance():
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
	if dist < 5:
		present = True
		return dist
	return dist
	

try:
	# while present == False:
	# 	dist = distance()
	# 	print ("Measured Distance = %.1f cm" % dist)
	# 	if dist < 5:
	# 		break
	# 	time.sleep(1)

	# Reset by pressing CTRL + C
except KeyboardInterrupt:
	print("Measurement stopped by User")
	GPIO.cleanup()
