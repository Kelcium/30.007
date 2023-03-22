import RPi.GPIO as GPIO
# https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/


import time


# We are going to use the BCM not BOARD layout
# https://i.stack.imgur.com/yHddo.png - BCM are the "GPIO#" ones not the ordered pins
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

while 1:

  for x in range(100):
    print("Speeding up " + str(x))
    rpwm.ChangeDutyCycle(x)
    time.sleep(0.25)

  time.sleep(5)

  for x in range(100):

    print("Slowing down " + str(x))
    rpwm.ChangeDutyCycle(100-x)
    time.sleep(0.25)
