from MFRC522 import SimpleMFRC522

#firebase access
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("airportkiosk30007-fc33c6c8bf96.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
