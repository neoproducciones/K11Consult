#!/usr/bin/env python
#
# Raspberry Pi Rotary Test Encoder Class
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# This class uses a standard rotary encoder with push switch
#

import sys
import time
from rotary_class import RotaryEncoder

# Define GPIO inputs
PIN_A = 11  # DT
PIN_B = 13  # CLK
BUTTON = 12  # SW

contador = 0

# This is the event callback routine to handle events
def switch_event(event):
    global contador
    if event == RotaryEncoder.CLOCKWISE:
        print "Clockwise"
        contador += 1
    elif event == RotaryEncoder.ANTICLOCKWISE:
        print "Anticlockwise"
        contador -= 1
    elif event == RotaryEncoder.BUTTONDOWN:
        print "Button down"
    elif event == RotaryEncoder.BUTTONUP:
        print "Button up"

    print contador

    return


# Define the switch
rswitch = RotaryEncoder(PIN_A, PIN_B, BUTTON, switch_event)

while True:
    time.sleep(100000)