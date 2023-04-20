import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#PUL = 18  #main
#PUL = 17 #drop
#PUL = 4  #sub
PUL = 22 #elevator
DIR = 27

GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)

GPIO.output(DIR, GPIO.HIGH)

print("going up")
for x in range(9000):
	GPIO.output(PUL, GPIO.HIGH)
	time.sleep(0.0003)
	GPIO.output(PUL, GPIO.LOW)
	time.sleep(0.0003)
