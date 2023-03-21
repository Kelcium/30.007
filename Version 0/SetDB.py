import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
# import RPi.GPIO as GPIO
# from mfrc522 import SimpleMFRC522

# reader = SimpleMFRC522()

cred = credentials.Certificate(r"test-5b286-firebase-adminsdk-prj2f-ad65922631.json")
firebase_admin.initialize_app(cred, {'databaseURL' : 'https://test-5b286-default-rtdb.asia-southeast1.firebasedatabase.app/'})
ref = db.reference("/")
with open(r"C:\Users\ethan\Downloads\test.json", "r") as f:
    file_contents = json.load(f)
ref.set(file_contents)

# for _ in range(3):
    #disable all RFID RST pins except storage 1
