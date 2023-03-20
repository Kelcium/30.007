import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json


cred = credentials.Certificate(r"C:\Users\Ethan\Downloads\test-5b286-firebase-adminsdk-prj2f-8ce04accb3.json")
# firebase_admin.initialize_app(cred, {'databaseURL' : 'https://test-5b286-default-rtdb.asia-southeast1.firebasedatabase.app/'})
ref = db.reference("/")
with open(r"C:\Users\Ethan\Downloads\database.json", "r") as f:
    file_contents = json.load(f)

ref.set(file_contents)