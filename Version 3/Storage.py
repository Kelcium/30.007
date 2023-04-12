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
#nfc.addBoard("Storage 1", 12)
#nfc.addBoard("Storage 2", 13)
#nfc.addBoard("Storage 3", 16)
#nfc.addBoard("Storage Test", 25)
#storage_id = ["Storage 1", "Storage 2", "Storage 3", "Storage Test"]
#storage_id = ["Storage Test"]
#storage_luggage = {}
#nfc.addBoard("Elevator", 5)
#for compartment in storage_id:
#	print(compartment)
#	id_, luggagenum = nfc.RFID_storage(compartment)
#	if luggagenum == None:
#		print("Compartment Empty!")
#	else:
#		storage_luggage[id_] = luggagenum
#		f.data_edit(compartment, id_)

#print(storage_luggage)
print(nfc.boards)
#f.Arduino("Initialising!")
f.SetDB()
#ref = db.reference("/").get()

while True:
        ref = db.reference("/").get()
#        f.Arduino("Please scan passport!")
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
                    print("No baggage to collect!")
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
#                            f.Arduino("Dispensing")
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
                f.Arduino("Please hold!")
