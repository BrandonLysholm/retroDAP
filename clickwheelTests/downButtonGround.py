import RPi.GPIO as GPIO
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, GPIO.PUD_UP)

while True:
    if GPIO.input(11) == GPIO.LOW:
        print("down button was pressed")
        time.sleep(1) #sleeping for one second after button is pressed
        print("ended wait")



