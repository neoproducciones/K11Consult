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

import sys, time#, os, serial
import memdata
import serialThread

#PORT = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
PORT = ""
memdata.init()
incomingData = serialThread.ReadStream(PORT, True)

print("Esperando al hijo")
j = 0
while j<100:
    #if (incomingData.getIntegrity):
    print(memdata.D['RPM'])
    j = j+1

#PORT.write('\x30')
#PORT.flushInput()
sys.exit()

