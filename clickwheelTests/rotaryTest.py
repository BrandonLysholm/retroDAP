# Author: Brandon Lysholm
# This program detects when the rotary encoder starts spinning, and it will read as spinning
# until it gets spun one click the other direction

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(33, GPIO.IN, GPIO.PUD_UP)

while True:
    if GPIO.input(33) == GPIO.HIGH:
        print("Spinning")
        time.sleep(1)
        print("end sleep")
