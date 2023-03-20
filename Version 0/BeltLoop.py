#import RPi.GPIO as GPIO
from functions import passenger
import MFRC522
import signal
import time

#program called with RFID as arg
reader = SimpleMFRC522()
GPIO.setmode(GPIO.Board)
GPIO.setup({motorpin}, GPIO.OUT)
GPIO.setup({laserpin}, GPIO.IN)
tray_present = GPIO.input({laserpin})

kiosk_read = True

#connecting to Firestore, if init doesn't do it properly
#db = firestore.client()

#object of kiosk reader
#kiosk_reader = MFRC522.MFRC522()

while kiosk_read == True and tray_present == False:
    kiosk_read = False

    id, passenger = reader.read()

    data = db.collection.document(text).get("luggage")
    print(data)

    GPIO.cleanup()


