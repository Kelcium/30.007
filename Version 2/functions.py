import RPi.GPIO as GPIO
# https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
import time
from mfrc522 import SimpleMFRC522
import spidev
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import ST7735

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
	rpwm.start(0)
	lpwm.start(0)
	
	rpwm.ChangeDutyCycle(x)
	time.sleep(0.5)

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

class NFC():
    def __init__(self, bus=0, device=0, spd=1000000):
        GPIO.setmode(GPIO.BCM)
        self.reader = SimpleMFRC522()
        self.close()
        self.boards = {}
        
        self.bus = bus
        self.device = device
        self.spd = spd

    def reinit(self):
        self.reader.READER.spi = spidev.SpiDev()
        self.reader.READER.spi.open(self.bus, self.device)
        self.reader.READER.spi.max_speed_hz = self.spd
        self.reader.READER.MFRC522_Init()

    def close(self):
        self.reader.READER.spi.close()

    def addBoard(self, rid, pin):
        GPIO.setup(pin, GPIO.OUT)
        self.boards[rid] = pin

    def selectBoard(self, rid):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.boards[rid], GPIO.OUT)
        if not rid in self.boards:
            print("readerid " + rid + " not found")
            return False

        for loop_id in self.boards:
            GPIO.output(self.boards[loop_id], loop_id == rid)
        return True

    def write(self, rid, value):
        if not self.selectBoard(rid):
            return False

        self.reinit()
        self.reader.write_no_block(value)
        self.close()
        return True

    def RFID_kiosk(self, rid):
        if not self.selectBoard(rid):
            return None

        self.reinit()
        print("reinitialised")
        try:
            id_, passportnum = self.reader.read()
            passportnum = passportnum.strip()
        finally:
            GPIO.cleanup()
            return id_, passportnum
