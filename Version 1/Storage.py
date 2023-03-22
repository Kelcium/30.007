import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from functions import Queue
from ultrasonic import distance_check

# ultrasound setup for belt

q = Queue()
reader = SimpleMFRC522()

cred = credentials.Certificate(r"test-5b286-firebase-adminsdk-prj2f-ad65922631.json")
firebase_admin.initialize_app(cred, {'databaseURL' : 'https://test-5b286-default-rtdb.asia-southeast1.firebasedatabase.app/'})
#ref = db.reference("/").get()

while True:
        ref = db.reference("/").get()
        try:
                id_, passportnum = reader.read()
                passportnum = passportnum.strip()
                print(passportnum)
        finally:
                GPIO.cleanup()

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
            else:
                sorted_by_size = sorted(not_dispensed, key=lambda x: x["Size"])[::-1]
                for bag in sorted_by_size:
                    q.enqueue(bag)
                    
                while q.size > 0:

                    if True:
                        bag = q.dequeue()
                        storage = bag["Storage"]
                        print("Dispensing new luggage")
                        dist, present = distance_check()
                        while present == False:
                            dist, present = distance_check()
                            print("Measured Distance = %.1f cm" % dist)
                            if dist < 5:
                                break
                        # ServoID[storage].open
                        count = update_true.pop()
                        print(ref[passportnum][count]["Dispensed"])
                        db.reference(f"/{passportnum}/{count}").update({"Dispensed" : "True"})
                        time.sleep(5)
                        # ServoID[storage].close
                    #run storage file with passportnum as argument
        else:
                print("No baggage to collect")

# if len(ref[passportnum]) > 1:
#     sorted_by_size = sorted(ref[passportnum], key = lambda x:x["Size"])[::-1]
#     for bag in sorted_by_size:
#         q.enqueue(bag)
#
# count = 0
# while q.size > 0:
#
#     if True:
#         bag = q.dequeue()
#         storage = bag["Storage"]
#         # ServoID[storage].open
#         sorted_by_size[count]["Dispensed"] = "True"
#         db.reference("/").update({passportnum: sorted_by_size})
#         time.sleep(5)
#         # ServoID[storage].close
#         count += 1
