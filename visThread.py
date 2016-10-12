#!/usr/bin/python

# Copyright (C) 2016 Javier Nuevo - www.facebook.com/neoproducciones

import sys, time, math, threading, datetime
import memdata


class visThread(threading.Thread):
    def __init__(self):

        self.screenlines = ''

        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):

        while memdata.vis:
            create_screen(self)
            console_send(screenlines)
            lcd_send(screenlines)
            sleep(memdata.vis_ms)
        sleep(1)

    def create_screen(self):
        -  Método: convierte valores a cadena 9 caracteres "XXX NNNNN"

        Primera pantalla

        1-Velocidad  2-Consumo instantáneo
        3-RPM        4-Avance encendido
        5-Temperat.  6-Oxígeno
        7-Batería    8-MAF

        Segunda pantalla

        

       - memdata.D['RPM'] = int(round((readvalues[0] * 12.5), 2))
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

