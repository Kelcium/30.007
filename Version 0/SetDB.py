import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json


cred = credentials.Certificate(r"C:\Users\ethan\Downloads\test-5b286-firebase-adminsdk-prj2f-ad65922631.json")
firebase_admin.initialize_app(cred, {'databaseURL' : 'https://test-5b286-default-rtdb.asia-southeast1.firebasedatabase.app/'})
ref = db.reference("/")
with open(r"C:\Users\ethan\Downloads\test.json", "r") as f:
    file_contents = json.load(f)

ref.set(file_contents)