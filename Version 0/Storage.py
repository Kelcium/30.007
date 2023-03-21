import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

class Queue():
    
    def __init__(self):
        self.__items = []
        
    def enqueue(self, item):
        self.__items.append(item)
        
    def dequeue(self):
        if self.size > 0:
            return self.__items.pop(0)
        
    def peek(self):
        if self.size > 0:
            return self.__items[0]

    @property    
    def size(self):
        return len(self.__items)
    
q = Queue()
reader = SimpleMFRC522()

reader = SimpleMFRC522()
cred = credentials.Certificate(r"test-5b286-firebase-adminsdk-prj2f-ad65922631.json")
firebase_admin.initialize_app(cred, {'databaseURL' : 'https://test-5b286-default-rtdb.asia-southeast1.firebasedatabase.app/'})
ref = db.reference("/").get()

while True:

        try:
                id_, passportnum = reader.read()
                passportnum = passportnum.strip()
        finally:
                GPIO.cleanup()
        
        if passportnum in ref.keys():
            sorted_by_size = sorted(ref[passportnum], key=lambda x: x["Size"])[::-1]
            for bag in sorted_by_size:
                q.enqueue(bag)

            count = 0
            while q.size > 0:

                if True:
                    bag = q.dequeue()
                    storage = bag["Storage"]
                    # ServoID[storage].open
                    sorted_by_size[count]["Dispensed"] = "True"
                    db.reference("/").update({passportnum: sorted_by_size})
                    time.sleep(5)
                    # ServoID[storage].close
                    count += 1
                #run storage file with passportnum as argument
        else:
                print("No baggage to collect")
                break

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
