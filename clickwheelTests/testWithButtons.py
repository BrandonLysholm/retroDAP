#Original source: https://github.com/nstansby/rpi-rotary-encoder-python.git
# Sample code to demonstrate Encoder class.  Prints the value every 5 seconds, and also whenever it changes.

import time
import RPi.GPIO as GPIO
from fullEncoder import FullEncoder

def valueChanged(value, direction):
    print("* New value: {}, Direction: {}".format(value, direction))

def btnChange(btn):
    print("Button pressed was ", btn)

GPIO.setmode(GPIO.BOARD)

e1 = FullEncoder(32, 33, 10, 11, 7, 15, 16, btnChange, valueChanged)

try:
    while True:
        time.sleep(5)
        print("Value is {}".format(e1.getValue()))
except Exception:
    pass

GPIO.cleanup()
