# Author: Brandon Lysholm

import RPi.GPIO as GPIO
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, GPIO.PUD_UP) #center
GPIO.setup(11, GPIO.IN, GPIO.PUD_UP) #down
GPIO.setup(7, GPIO.IN, GPIO.PUD_UP) #right
GPIO.setup(15, GPIO.IN, GPIO.PUD_UP) #up
GPIO.setup(16, GPIO.IN, GPIO.PUD_UP) #left

print("Ready for input")

while True:
    #Handling each button is else if
    if GPIO.input(10) == GPIO.LOW:
        print("Center button was pushed")
        time.sleep(.25) #Sleeping for 1/4 second
        print("Ready for next input")
    elif GPIO.input(11) == GPIO.LOW:
        print("Down button was pushed")
        time.sleep(.25) #Sleeping for 1/4 second
        print("Ready for next input")
    elif GPIO.input(7) == GPIO.LOW:
        print("Right button was pushed")
        time.sleep(.25) #Sleeping for 1/4 second
        print("Ready for next input")
    elif GPIO.input(15) == GPIO.LOW:
        print("Up button was pushed")
        time.sleep(.25) #Sleeping for 1/4 second
        print("Ready for next input")
    elif GPIO.input(16) == GPIO.LOW:
        print("Left button was pushed")
        time.sleep(.25) #Sleeping for 1/4 second
        print("Ready for next input")






