#!/usr/bin/python

# LCD visualization and encoder user interface

# Copyright (C) 2016 Javier Nuevo - www.facebook.com/neoproducciones

import sys, time, math, threading, datetime
import memdata
if memdata.lcd:
    import liquidcrystal_i2c


class VisThread(threading.Thread):
    def __init__(self):

        self.sbuf = ""
        # Screen lines buffer. Each line is 18 usable chars

        self.viewport = 0
        self.old_viewport = 0
        # Number of the current and former screen.

        self.rows = 4
        self.cols = 20
        # Screen size

        self.sensor_len = 10
        self.sensors_per_display = 8

        if memdata.lcd:
            self.lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=self.rows)
        # We create an instance of the LCD screen driver

        self.sbuf = "      __ __         " + "|\ ||(_ (_  /\ |\ | " + "| \||__)__)/--\| \| " + "                    "
        self.lcd_send()
        time.sleep(2)

        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while memdata.vis:
            self.write_scr_buffer()
            self.lcd_send()

    def write_scr_buffer(self):
        # We create the whole screen buffer as one line
        self.sbuf = ""
        for k, v in memdata.D.items():
            self.sbuf += (" " + k + ":" + str(v).rjust(5))
        # Here and on we can write the engine error codes.
        # We must assure the screen buffer length is a multiple of rows*col

    def lcd_send(self):
        start = self.viewport * self.sensors_per_display * self.sensor_len
        for i in range(4):
            end = start + self.cols
            linea = self.sbuf[start:end]
            if memdata.lcd:
                self.lcd.printline(i, linea)
            else:
                print (linea)
            start += self.cols
