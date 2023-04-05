import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
import RPi.GPIO as GPIO
#from mfrc522 import SimpleMFRC522
import functions as f
import ST7735

GPIO.setwarnings(True)
q = f.Queue()
nfc = f.NFC()
nfc.addBoard("RFID_kiosk", 25)
print(nfc.boards)
cred = credentials.Certificate(r"test-5b286-firebase-adminsdk-prj2f-ad65922631.json")
firebase_admin.initialize_app(cred, {'databaseURL' : 'https://test-5b286-default-rtdb.asia-southeast1.firebasedatabase.app/'})
#ref = db.reference("/").get()

while True:
        ref = db.reference("/").get()
        id_, passportnum = nfc.RFID_kiosk("RFID_kiosk")
        print(passportnum)
        not_dispensed = []
        update_true = []
        if passportnum in ref.keys():
            for i in range(len(ref[passportnum])):
                if ref[passportnum][i]["Dispensed"] == "False":
                    not_dispensed.append(ref[passportnum][i])
                    update_true.append(i)
            print(not_dispensed)
            if len(not_dispensed) == 0:
                    print("No baggage to collect")
                    pass
            else:
                sorted_by_size = sorted(not_dispensed, key=lambda x: x["Size"])[::-1]
                for bag in sorted_by_size:
                    q.enqueue(bag)
                    
                while q.size > 0:

                    if True:
                        bag = q.dequeue()
                        storage = bag["Storage"]
                        print(storage)
                        print("Dispensing new luggage")
                        f.servo_control(storage, True)
                        dist, present = f.distance_check(23, 24)
                        while present == False:
                            f.belt_move(1)
                            dist, present = f.distance_check(23, 24)
                        f.belt_move(0)
                        count = update_true.pop()
                        print(ref[passportnum][count]["Dispensed"])
                        db.reference(f"/{passportnum}/{count}").update({"Dispensed" : "True"})
                        time.sleep(5)
                print("All luggage dispensed")
        else:
                print("No baggage to collect")
