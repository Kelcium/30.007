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

	PUL = 17;  # GPIO pin 17 to the RPWM on the BTS7960
	DIR = 27;  # GPIO pin 28 to the LPWM on the BTS7960
	EN = 22;  # connect GPIO pin 27 to L_EN on the BTS796


	# Set all of our PINS to output
	GPIO.setup(PUL, GPIO.OUT)
	GPIO.setup(DIR, GPIO.OUT)
	GPIO.setup(EN, GPIO.OUT)

	GPIO.output(DIR, GPIO.HIGH)
	GPIO.output(EN, GPIO.HIGH)

	if x == 1:
		GPIO.output(L_EN, GPIO.HIGH)
		GPIO.PWM(PUL, 100)
	
	if x == 0:
		GPIO.output(L_EN, GPIO.LOW)
	
	time.sleep(0.5)

def distance_check():
	GPIO.setmode(GPIO.BCM)
	TRIG = 23
	GPIO.setup(TRIG, GPIO.OUT)
	ECHO = 24
	GPIO.setup(ECHO, GPIO.IN)
	
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
        try:
            id_, passportnum = self.reader.read()
            passportnum = passportnum.strip()
        finally:
            GPIO.cleanup()
            return id_, passportnum
