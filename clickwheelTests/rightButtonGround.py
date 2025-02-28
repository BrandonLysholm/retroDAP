# Author: Brandon Lysholm

import RPi.GPIO as GPIO
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, GPIO.PUD_UP)

while True:
    if GPIO.input(7) == GPIO.LOW:
        print("right button was pressed")
        time.sleep(1) #sleeping for one second after button is pressed
        print("ended wait")



