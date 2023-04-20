from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)

PUL = 17;  # GPIO pin 17 to the RPWM on the BTS7960
DIR = 27;  # GPIO pin 28 to the LPWM on the BTS7960
EN = 22;  # connect GPIO pin 27 to L_EN on the BTS796


# Set all of our PINS to output
 
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT)

GPIO.output(DIR, GPIO.HIGH)
GPIO.output(EN, GPIO.HIGH)

while True:
		GPIO.output(PUL, GPIO.HIGH)
		sleep(0.0005)
		GPIO.output(PUL, GPIO.LOW)
		sleep(0.0005)
