import RPi.GPIO as GPIO
import time

TRIG = 23
GPIO.setup(TRIG, GPIO.OUT)
ECHO = 24
GPIO.setup(ECHO, GPIO.IN)

while True:
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
			print("Measured Distance = %.1f cm" % dist)
