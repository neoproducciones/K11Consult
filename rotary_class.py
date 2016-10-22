#!/usr/bin/env python
#
# Raspberry Pi Rotary Encoder Class
# $Id: rotary_class.py,v 1.2 2014/01/31 13:34:48 bob Exp $
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# This class uses standard rotary encoder with push switch
# 
#

import RPi.GPIO as GPIO


class RotaryEncoder:
    CLOCKWISE = 1
    ANTICLOCKWISE = 2
    BUTTONDOWN = 3
    BUTTONUP = 4

    rotary_a = 0
    rotary_b = 0
    rotary_c = 0
    last_state = 0
    direction = 0

    # Initialise rotary encoder object
    def __init__(self, pinA, pinB, button, callback):
        self.pinA = pinA
        self.pinB = pinB
        self.button = button
        self.callback = callback
        self.primero = True # Adding this because it's a two changes per detent encoder

        GPIO.setmode(GPIO.BOARD) # Changed from the original GPIO.BCM for easier naming

        # The following lines enable the internal pull-up resistors
        # on version 2 (latest) boards
        GPIO.setwarnings(False)
        GPIO.setup(self.pinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # For version 1 (old) boards comment out the above four lines
        # and un-comment the following 3 lines
        # GPIO.setup(self.pinA, GPIO.IN)
        # GPIO.setup(self.pinB, GPIO.IN)
        # GPIO.setup(self.button, GPIO.IN)

        # Add event detection to the GPIO inputs
        # Tuning different bouncetime values to avoid false readings
        GPIO.add_event_detect(self.pinA, GPIO.FALLING, callback=self.switch_event_A, bouncetime=100)
        # GPIO.add_event_detect(self.pinB, GPIO.FALLING, callback=self.switch_event_B, bouncetime=10)
        GPIO.add_event_detect(self.button, GPIO.BOTH, callback=self.button_event, bouncetime=50)
        return

    # Call back routine called by switch events
    def switch_event_A(self, switch):
        if GPIO.input(self.pinB):
            event=self.CLOCKWISE
        else:
            event=self.ANTICLOCKWISE

        self.callback(event)


    # Push button up event
    def button_event(self, button):
        if GPIO.input(button):
            event = self.BUTTONUP
        else:
            event = self.BUTTONDOWN
        self.callback(event)
        return

    # Get a switch state
    def getSwitchState(self, switch):
        return GPIO.input(switch)

# End of RotaryEncoder class
