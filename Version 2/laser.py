import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

laser = 5
buzzer = 26
GPIO.setup(laser, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(laser, False)
GPIO.output(buzzer, False)

while True:
	try:
		GPIO.output(laser, True)
		GPIO.output(buzzer, True)
		sleep(0.5)
		GPIO.output(buzzer, False)
		sleep(0.05)
		GPIO.output(buzzer, True)
		sleep(0.5)
		GPIO.output(buzzer, False)
		sleep(0.05)
		GPIO.output(buzzer, True)
		sleep(0.5)
		GPIO.output(buzzer, False)
		sleep(0.05)
		GPIO.output(buzzer, True)
		sleep(0.1)
		GPIO.output(buzzer, False)
		sleep(0.05)
		GPIO.output(buzzer, True)
		sleep(0.1)
		GPIO.output(buzzer, False)
		sleep(0.05)
		GPIO.output(buzzer, True)
		sleep(0.1)
		GPIO.output(buzzer, False)
		sleep(0.05)
		GPIO.output(buzzer, True)
		sleep(0.5)
		GPIO.output(buzzer, False)
		sleep(0.05)
		GPIO.output(buzzer, True)
		sleep(0.5)
		GPIO.output(buzzer, False)
		sleep(0.05)
		GPIO.output(buzzer, True)
		sleep(0.5)
		GPIO.output(buzzer, False)
		sleep(0.05)
		
		
	except:
		GPIO.output(laser, False)
		GPIO.output(buzzer, False)
		GPIO.cleanup()
