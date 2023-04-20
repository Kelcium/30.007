#!/usr/bin/env python3
import serial
import time

def Arduino(text):
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()

    while True:
        ser.write(text.encode())
        print(text)
        time.sleep(1)


Arduino("Initialising!\n")
