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

PORT = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
incomingData = serialThread.ReadStream(PORT,True)

global RPM_Value

while True:

    if (incomingData.getIntegrity):

        println (RPM_Value)

    #time.sleep(0.02)

PORT.write('\x30')
PORT.flushInput()
sys.exit()

