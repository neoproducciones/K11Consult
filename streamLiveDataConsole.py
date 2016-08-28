#!/usr/bin/python
# streamLiveDataConsole.py

#Copyright (C) 2015 Eilidh Fridlington http://eilidh.fridlington.com

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>

import os
import sys
import serial
import serialThread
from dials import *

PORT = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
incomingData = serialThread.ReadStream(PORT,True)

MPH_Value = 0
RPM_Value = 0
TEMP_Value = 0
BATT_Value = 0
AAC_Value = 0
MAF_Value = 0

while True:

    MPH_Value = incomingData.returnMPH()
    RPM_Value = incomingData.returnRPM()
    TEMP_Value = incomingData.returnTEMP()
    BATT_Value = incomingData.returnBATT()
    AAC_Value = incomingData.returnAAC()
    MAF_Value = incomingData.returnMAF()

    print MPH_Value
    print RPM_Value
    print TEMP_Value
    print BATT_Value
    print AAC_Value
    print MAF_Value

    #time.sleep(0.02)

PORT.write('\x30')
PORT.flushInput()
sys.exit()

