#!/usr/bin/python
# main.py

import sys
import time  # os,
import memdata
memdata.init()

import VisThread

if memdata.usb:
    import os
    import serial
    import SerialThread

    PORT = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
    t_serial = SerialThread.SerialThread(PORT, True)
else:
    PORT = ""

if memdata.db:
    import dbThread
    # t_db = dbThread.dbThread()

t_vis = VisThread.VisThread()

print("Waiting for child process")
j = 0
while j<10000:
    j = j+1
    time.sleep (1)

if memdata.usb:
    PORT.write('\x30')
    PORT.flushInput()
sys.exit()

