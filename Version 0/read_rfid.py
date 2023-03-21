#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

reader = SimpleMFRC522()
cred = credentials.Certificate(r"test-5b286-firebase-adminsdk-prj2f-ad65922631.json")
firebase_admin.initialize_app(cred, {'databaseURL' : 'https://test-5b286-default-rtdb.asia-southeast1.firebasedatabase.app/'})
ref = db.reference("/").get()

while True:

        try:
                id, passportnum = reader.read()
        finally:
                GPIO.cleanup()

        if passportnum in ref.keys():
                #run storage file with passportnum as argument
        else:
                print("No baggage to collect")
        break


