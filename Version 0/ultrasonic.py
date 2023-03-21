import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 23
GPIO.setup(TRIG, GPIO.OUT)

ECHO = 24
GPIO.setup(ECHO, GPIO.IN)

print("Distance measurement in progress")
while True:
    GPIO.output(TRIG, False)
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        start = time.time()

    while GPIO.input(ECHO) == 1:
        end = time.time()

    duration = end - start
    dist = duration * 17500
    dist = round(dist, 2)
    print("Distance: ",dist,"cm")

    GPIO.cleanup()
