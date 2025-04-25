# Original source: https://github.com/nstansby/rpi-rotary-encoder-python.git
# Modified by Brandon Lysholm to include the five buttons on the navigation wheel
# Class to monitor a rotary encoder and update a value.  You can either read the value when you need it, by calling getValue(), or
# you can configure a callback which will be called whenever the value changes.

import RPi.GPIO as GPIO

class FullEncoder:

    def __init__(self, leftPin, rightPin, cBtn, dBtn, rBtn, uBtn, lBtn, holdSwitch, callback=None):
        # Setting GPIO mode
        GPIO.setmode(GPIO.BOARD)
        # Original code declaring rotary encoders
        self.leftPin = leftPin
        self.rightPin = rightPin
        # Added functionality of buttons
        self.cBtn = cBtn
        self.dBtn = dBtn
        self.rBtn = rBtn
        self.uBtn = uBtn
        self.lBtn = lBtn
        # Original code adding functionality to get information for rotary encoder
        self.value = 0
        self.state = '00'
        self.direction = None
        self.callback = callback
        GPIO.setup(self.leftPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.rightPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.leftPin, GPIO.BOTH, callback=self.transitionOccurred)  
        GPIO.add_event_detect(self.rightPin, GPIO.BOTH, callback=self.transitionOccurred)
        # Initializing the buttons as inputs
        GPIO.setup(self.cBtn, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.dBtn, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.rBtn, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.uBtn, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.lBtn, GPIO.IN, GPIO.PUD_UP)
        # Setting watchers on the buttons
        GPIO.add_event_detect(self.cBtn, GPIO.FALLING, callback=self.btnPress)
        GPIO.add_event_detect(self.dBtn, GPIO.FALLING, callback=self.btnPress)
        GPIO.add_event_detect(self.rBtn, GPIO.FALLING, callback=self.btnPress)
        GPIO.add_event_detect(self.uBtn, GPIO.FALLING, callback=self.btnPress)
        GPIO.add_event_detect(self.lBtn, GPIO.FALLING, callback=self.btnPress)
        # Adding functionality for hold switch
        self.holdSwitch = holdSwitch
        GPIO.setup(self.holdSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)



    #Code added to detect a button press
    def btnPress(self, channel):
        btnPressed = "unknown"
        cPin = GPIO.input(self.cBtn)
        dPin = GPIO.input(self.dBtn)
        rPin = GPIO.input(self.rBtn)
        uPin = GPIO.input(self.uBtn)
        lPin = GPIO.input(self.lBtn)

        # Handling the hold switch first
        holdSwitch = GPIO.input(self.holdSwitch)

        # if holdSwitch == GPIO.HIGH:
            # btnPressed = "unlocked"
        # elif holdSwitch == GPIO.LOW:
        if holdSwitch == GPIO.LOW:
            btnPressed = "locked"
        elif cPin == GPIO.LOW:
            btnPressed = "center"
        elif dPin == GPIO.LOW:
            btnPressed = "down"
        elif rPin == GPIO.LOW:
            btnPressed = "right"
        elif uPin == GPIO.LOW:
            btnPressed = "up"
        elif lPin == GPIO.LOW:
            btnPressed = "left"


        self.callback(btnPressed)

    def transitionOccurred(self, channel):
        p1 = GPIO.input(self.leftPin)
        p2 = GPIO.input(self.rightPin)
        newState = "{}{}".format(p1, p2)

        # Handling the hold switch first
        holdSwitch = GPIO.input(self.holdSwitch)

        if holdSwitch == GPIO.LOW:
            return

        if self.state == "00": # Resting position
            if newState == "01": # Turned right 1
                self.direction = "R"
            elif newState == "10": # Turned left 1
                self.direction = "L"

        elif self.state == "01": # R1 or L3 position
            if newState == "11": # Turned right 1
                self.direction = "R"
            elif newState == "00": # Turned left 1
                if self.direction == "L":
                    self.value = self.value - 1
                    if self.callback is not None:
                        self.callback(self.direction)

        elif self.state == "10": # R3 or L1
            if newState == "11": # Turned left 1
                self.direction = "L"
            elif newState == "00": # Turned right 1
                if self.direction == "R":
                    self.value = self.value + 1
                    if self.callback is not None:
                        self.callback(self.direction)

        else: # self.state == "11"
            if newState == "01": # Turned left 1
                self.direction = "L"
            elif newState == "10": # Turned right 1
                self.direction = "R"
            elif newState == "00": # Skipped an intermediate 01 or 10 state, but if we know direction then a turn is complete
                if self.direction == "L":
                    self.value = self.value - 1
                    if self.callback is not None:
                        self.callback(self.direction)
                elif self.direction == "R":
                    self.value = self.value + 1
                    if self.callback is not None:
                        self.callback(self.direction)
                
        self.state = newState

    def getValue(self):
        return self.value
