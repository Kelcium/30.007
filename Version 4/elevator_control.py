import RPi.GPIO as GPIO
import time
import pygame

pygame.init()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PUL = 18  #temp
#PUL = 17  #true
DIR = 27
EN = 22

GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT)

GPIO.output(EN, GPIO.HIGH)

done =

while True:
	pressed_keys = pygame.key.get_pressed()
	if pressed_keys[K_UP]:
		GPIO.output(DIR, GPIO.HIGH)
		GPIO.output(PUL, GPIO.HIGH)
		time.sleep(0.0001)
		GPIO.output(PUL, GPIO.LOW)
		time.sleep(0.0001)
	elif pressed_keys[K_DOWN]:
		GPIO.output(DIR, GPIO.LOW)
		GPIO.output(PUL, GPIO.HIGH)
		time.sleep(0.0001)
		GPIO.output(PUL, GPIO.LOW)
		time.sleep(0.0001)
