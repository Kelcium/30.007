import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import functions

#program called with RFID as arg
kiosk = MFRC522.MFRC522()
GPIO.setmode(GPIO.Board)
GPIO.setup({motorpin}, GPIO.OUT)
GPIO.setup({laserpin}, GPIO.IN)

kiosk_reading = True

collection = Passenger(db.collection('YanHan'))
print(collection.name)
print(collection.luggage_queue)
