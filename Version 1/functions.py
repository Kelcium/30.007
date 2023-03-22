import RPi.GPIO as GPIO
# https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
import time

class Queue():

    def __init__(self):
        self.__items = []

    def enqueue(self, item):
        self.__items.append(item)

    def dequeue(self):
        if self.size > 0:
            return self.__items.pop(0)

    def peek(self):
        if self.size > 0:
            return self.__items[0]

    @property
    def size(self):
        return len(self.__items)

def belt_move(x):
	GPIO.setmode(GPIO.BCM)  
	GPIO.setwarnings(False)

	RPWM = 17;  # GPIO pin 17 to the RPWM on the BTS7960
	LPWM = 18;  # GPIO pin 28 to the LPWM on the BTS7960

	# For enabling "Left" and "Right" movement
	L_EN = 27;  # connect GPIO pin 27 to L_EN on the BTS7960
	R_EN = 22;  # connect GPIO pin 22 to R_EN on the BTS7960


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
	time.sleep(0.25)

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

	if dist < 5:
		return dist, True
	return dist, False
