import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import time


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

cred = credentials.Certificate(r"C:\Users\Ethan\Downloads\test-5b286-firebase-adminsdk-prj2f-8ce04accb3.json")
# firebase_admin.initialize_app(cred, {'databaseURL' : 'https://test-5b286-default-rtdb.asia-southeast1.firebasedatabase.app/'})
ref = db.reference("/").get()

while True:
    
    passportnum = "Passport Number 1"
    if passportnum in ref.keys():
        break


if len(ref[passportnum]) > 1:
    sorted_by_size = sorted(ref[passportnum], key = lambda x:x["Size"])[::-1]
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