from gpiozero import Servo
from time import sleep

servo = Servo(19)
servo_in = Servo(5)
val = 1
val_in = -1

for x in range(20):
	print("opening")
	val -= 0.1
	val_in += 0.1
	servo.value = val
	servo_in.value = val_in
	sleep(0.05)

sleep(3)

for x in range(20):
	val += 0.1
	val_in -= 0.1
	servo.value = val
	servo_in.value = val_in
	sleep(0.05)
print("Storage Closed")


