import RPi.GPIO as GPIO
From mf

#program called with RFID as arg
reader = SimpleMFRC522()
GPIO.setmode(GPIO.Board)
GPIO.setup({motorpin}, GPIO.OUT)
GPIO.setup({laserpin}, GPIO.IN)

while True:
    GPIO.output({motorpin}, GPIO.HIGH)
    if GPIO.input({laserpin}):
        GPIO.output({motorpin}, GPIO.LOW)
        id, text = reader.read()
        if id == arg:
            break
        else:
            GPIO.output({motorpin}. GPIO.HIGH)