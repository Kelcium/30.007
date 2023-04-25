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
#nfc.addBoard("1", 12)
#nfc.addBoard("2", 13)
#nfc.addBoard("3", 16)
#storage_id = ["1", "2", "3"]
storage_id = []
storage_luggage = {}
#nfc.addBoard("Elevator", 5)

for compartment in storage_id:
	print(compartment)
	id_, luggagenum = nfc.RFID_storage(compartment)
	if luggagenum == None:
		print("Compartment Empty!")
	else:
		stored = "Storage " + compartment
		storage_luggage[stored] = luggagenum
		f.data_edit(compartment, id_)

print(storage_luggage)
print(nfc.boards)
f.Arduino("Initialising!\n")
time.sleep(1)
f.SetDB()
print("Database initialised!")
#ref = db.reference("/").get()
steps = 0

while True:
        ref = db.reference("/").get()
        f.Arduino("Please scan passport!\n")
        id_, passportnum = nfc.RFID_kiosk("RFID_kiosk")
        #f.Arduino("Passport Scanned!\n")
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
                        print("Dispensing new luggage")
                        f.Arduino("Dispensing\n")
                        f.servo_control(storage, 1)
                        f.servo_control(storage, 0)
                        dist = f.distance_check(1, 6)
                        f.Arduino("Dispensing\n")
                        while dist > 8:
                            f.belt_move(1)
                            dist = f.distance_check(1, 6)
                        f.belt_move(0)
                        print("Drop Operating!")
                        f.drop_move()
                        print("Elevator Shifting!")
                        steps = f.elevator_move(steps)
                        count = update_true.pop()
                        print(ref[passportnum][count]["Dispensed"])
                        db.reference(f"/{passportnum}/{count}").update({"Dispensed" : "True"})
                        time.sleep(1)
                f.elevator_full(steps)
                f.dc_dispense("Open")
                print("All luggage dispensed")
                f.elevator_return()
                time.sleep(10)
                f.elevator_full(0)
                f.dc_dispense("Close")
                f.elevator_return()
        else:
                print("No baggage to collect")
                f.Arduino("Please hold!\n")
                time.sleep(3)
