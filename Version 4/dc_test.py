import RPi.GPIO as GPIO
import time

def dc_dispense(status):
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	
	RPWM = 6
	LPWM = 21
	R_EN = 12
	L_EN = 16
	
	GPIO.setup(RPWM, GPIO.OUT)
	GPIO.setup(LPWM, GPIO.OUT)
	GPIO.setup(L_EN, GPIO.OUT)
	GPIO.setup(R_EN, GPIO.OUT)
	
	GPIO.output(R_EN, True)
	GPIO.output(L_EN, True)
	
	rpwm= GPIO.PWM(RPWM, 100)
	lpwm= GPIO.PWM(LPWM, 100)
	
	rpwm.ChangeDutyCycle(0)
	lpwm.ChangeDutyCycle(0)
	rpwm.start(0)
	lpwm.start(0)
	
	if status == "Close":
		print("Elevator Opening!")
		rpwm.ChangeDutyCycle(50)
		lpwm.ChangeDutyCycle(0)
		time.sleep(3)
		rpwm.ChangeDutyCycle(0)
		lpwm.ChangeDutyCycle(0)
		time.sleep(1)
	
	if status == "Open":
		print("Elevator Closing!")
		rpwm.ChangeDutyCycle(0)
		lpwm.ChangeDutyCycle(50)
		time.sleep(3)
		rpwm.ChangeDutyCycle(0)
		lpwm.ChangeDutyCycle(0)
		time.sleep(1)

dc_dispense("Open")
#time.sleep(3)
dc_dispense("Close")
