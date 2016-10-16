#!/usr/bin/python

# Copyright (C) 2016 Javier Nuevo - www.facebook.com/neoproducciones

import sys, time, math, threading, datetime
import memdata


class visThread(threading.Thread):
    def __init__(self):

        self.sensors = list
        # List of all sensors. Each sensor is 9 chars

        self.sbuf = list
        # Screen lines buffer. Each line is 18 usable chars

        self.viewport = 0
        self.old_viewport = 0
        # Number of the current and former screen.

        self.rows = 4
        self.cols = 20
        # Screen size

        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while memdata.vis:
            update_screen(self)
            console_send(screenlines)
            lcd_send(screenlines)
            sleep(memdata.vis_ms)

    def populate_sensors_list(self):
        for sensor in memdata.D:
            
        self.sensors.append ("KMH:" + str(memdata.D['KMH']).rjust(5))
        self.sensors.append ("ECO:" + str(7.4).rjust(5))  #  Fake as ***
        self.sensors.append ("RPM:" + string(memdata.D['KMH']).rjust(5))

        return True

    def populate_screen_buffer(self):
        return True


    def update_screen(self):


        -  Método: Inserta valores en lista de sensores "XXX NNNNN"
        -  Método: Convierte lista de sensores en líneas

        Primera pantalla

        1-Velocidad  2-Consumo instantáneo
        3-RPM        4-Avance encendido
        5-Temperat.  6-Oxígeno
        7-Batería    8-MAF

        Segunda pantalla



       - memdata.D['RPM'] = int(round((readvalues[0] * 12.5), 0))
       - memdata.D['MAF'] = readvalues[1] * 5
       - memdata.D['TMP'] = readvalues[2] - 50
       - memdata.D['OXY'] = readvalues[3] * 10
       - memdata.D['KMH'] = int(round(readvalues[4] * 2))
       - memdata.D['BAT'] = round(((readvalues[5] * 80) / 1000), 1)
        memdata.D['THL'] = readvalues[6] * 20
        memdata.D['INJ'] = readvalues[7] / 100
       - memdata.D['TIM'] = 110 - readvalues[8]
        memdata.D['IDL'] = readvalues[9] / 2
        memdata.D['AFS'] = readvalues[10]
        memdata.D['AFL'] = readvalues[11]
        memdata.D['DR0'] = readvalues[12]
        memdata.D['DR1'] = readvalues[13]

        memdata.integrity = True
        return True

