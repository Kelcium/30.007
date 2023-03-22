import RPi.GPIO as GPIO

#program called with RFID as arg
# reader = SimpleMFRC522()
GPIO.setmode(GPIO.Board)
GPIO.setup({motorpin}, GPIO.OUT)
GPIO.setup({laserpin}, GPIO.IN)
tray_present = GPIO.input({laserpin})

kiosk_read = True

#connecting to Firestore, if init doesn't do it properly
#db = firestore.client()

#object of kiosk reader
#kiosk_reader = MFRC522.MFRC522()
print(db.collection('YanHan'))
collection = Passenger(db.collection('YanHan').get())
print(collection.name)
print(collection.luggage_queue)


