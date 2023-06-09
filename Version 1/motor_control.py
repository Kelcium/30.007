import RPi.GPIO as GPIO
# https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
import time

def belt_move(x):
	GPIO.setmode(GPIO.BCM)  
	GPIO.setwarnings(False)

	RPWM = 14;  # GPIO pin 17 to the RPWM on the BTS7960
	LPWM = 15;  # GPIO pin 28 to the LPWM on the BTS7960

	# For enabling "Left" and "Right" movement
	L_EN = 3;  # connect GPIO pin 27 to L_EN on the BTS7960
	R_EN = 2;  # connect GPIO pin 22 to R_EN on the BTS7960


	# Set all of our PINS to output
	GPIO.setup(RPWM, GPIO.OUT)
	GPIO.setup(LPWM, GPIO.OUT)
	GPIO.setup(L_EN, GPIO.OUT)
	GPIO.setup(R_EN, GPIO.OUT)

	# Enable "Left" and "Right" movement on the HBRidge
	GPIO.output(R_EN, True)
	GPIO.output(L_EN, True)
	rpwm= GPIO.PWM(RPWM, 100)
	lpwm= GPIO.PWM(LPWM, 100)
	rpwm.ChangeDutyCycle(0)
	rpwm.start(0)
	lpwm.ChangeDutyCycle(0)
	lpwm.start(0)
	
	rpwm.ChangeDutyCycle(x)
	time.sleep(0.1)
