import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

def las_event():
	print("laser not detected")

laser = 26
GPIO.setup(laser, GPIO.IN)
GPIO.remove_event_detect(laser)
GPIO.add_event_detect(laser,GPIO.FALLING,callback=las_event)
	
while True:
	print("laser detected")
	sleep(0.5)
