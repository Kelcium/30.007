import RPi.GPIO as GPIO
from gpiozero import Servo
# https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
import time
from mfrc522 import SimpleMFRC522
import spidev
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import ST7735
import time
from threading import Thread
import serial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

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

	PUL = 18  # GPIO pin 17 to the RPWM on the BTS7960
	DIR = 27  # GPIO pin 28 to the LPWM on the BTS7960
	EN = 22

	# Set all of our PINS to output
	
	GPIO.setup(PUL, GPIO.OUT)
	GPIO.setup(DIR, GPIO.OUT)
	GPIO.setup(EN, GPIO.OUT)

	GPIO.output(DIR, GPIO.HIGH)
	GPIO.output(EN, GPIO.HIGH)

	if x == 1:
		for n in range(500):
			GPIO.output(PUL, GPIO.HIGH)
			time.sleep(0.0005)
			GPIO.output(PUL, GPIO.LOW)
			time.sleep(0.0005)
	
	if x == 0:
		GPIO.cleanup()

def distance_check(TRIG, ECHO):
	print("Checking distance!")
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(TRIG, GPIO.OUT)
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
		print("The measured distance is ", dist, " !")
		return dist, True
	return dist, False
	
def laser_check(INPUT):
	print("Checking lasers!")
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(INPUT, GPIO.IN)
	
	while GPIO.input(INPUT) == 0:
		return False
	
	return True

def servo_control(LuggageNo, Open=False):
	GPIO.setmode(GPIO.BCM)
	print("Storage Opening!")
	if LuggageNo == 1:
		con = 19
	if LuggageNo == 2:
		con = 20
	if LuggageNo == 3:
		con = 21
		
	servo = Servo(con)
	print(Open)
	val = -1
	
	if Open == True:
		print("Storage for Luggage ", LuggageNo, " Opening!")
		servo.value = val
		for x in range(20):
			val += 0.1
			servo.value = val
			time.sleep(0.05)
		time.sleep(3)
		for x in range(20):
			val -= 0.1
			servo.value = val
			time.sleep(0.05)
		print("Storage Closed")
	GPIO.cleanup()

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
            
    def RFID_storage(self, rid):
        if not self.selectBoard(rid):
            return None
		
        self.reinit()
        try:
            id_, luggagenum = self.reader.read()
            luggagenum = luggagenum.strip()
        finally:
            GPIO.cleanup()
            return id_, luggagenum
	
    def RFID_elevator(self, rid):
        if not self.selectboard(rid):
            return None
		
        self.reinit()
        try:
            id_, compartment = self.reader.read()
            compartment = compartment.strip()
        finally:
            GPIO.cleanup()
            return compartment

def data_edit(compartment, id_):
	with open("test 1.json", "r") as testfile:
		data = json.load(testfile)
	
	for passport in data.keys():
		print(passport)
		for luggage in data[passport]:
			if luggage["Tray RFID"] == id_:
				luggage["Storage"] = compartment
				print(compartment)
				
	print(data)
			
	with open("test 1.json", "w") as testfile:
		json.dump(data, testfile)
		print("Database updated!")

def SetDB():
	cred = credentials.Certificate(r"test-5b286-firebase-adminsdk-prj2f-ad65922631.json")
	firebase_admin.initialize_app(cred, {'databaseURL' : 'https://test-5b286-default-rtdb.asia-southeast1.firebasedatabase.app/'})
	ref = db.reference("/")
	with open(r"test.json", "r") as f:
		file_contents = json.load(f)
	ref.set(file_contents)

def Arduino(text):
	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
	ser.reset_input_buffer()
	ser.write(text.encode())
	print(text)
	time.sleep(1)
