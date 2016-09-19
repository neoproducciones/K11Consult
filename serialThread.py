#!/usr/bin/python
# serialThread.py

# Copyright (C) 2014 Eilidh Fridlington http://eilidh.fridlington.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>


import time
import math
import threading
import datetime


class ReadStream(threading.Thread):
    def __init__(self, data, port, connected=True):
        self.port = port
        self.connected = connected
        self.stream = False
        self.integrity = False
        self.d = dict
        self.d = data

        self.d = {'RPM': 300, 'MAF': 0, 'TMP': 0, 'OXY': 0, 'KMH': 0, 'BAT': 0, 'THL': 0, 'INJ': 0, 'TIM': 0, 'IDL': 0,
                  'AFS': 0, 'AFL': 0, 'DR0': 0, 'DR1': 0}

        self.fileName = datetime.datetime.now().strftime("%d-%m-%y-%H-%M")

        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):

        while self.connected == False:

            self.port.write('\xFF\xFF\xEF')
            time.sleep(2)
            isConnected = self.port.inWaiting()

            if isConnected:
                ecuResponse = self.port.read(1)
                if ecuResponse == '\x10':
                    print('Correct reply from ECU, sending data...')
                    self.connected = True

                else:
                    print('Wrong reply from ECU')

            else:
                print('Trying to connect to ECU')
                self.port.write('\xFF\xFF\xEF')
                time.sleep(2)

        self.port.write(
            '\x5A\x01\x5A\x05\x5A\x08\x5A\x09\x5A\x0B\x5A\x0C\x5A\x0D\x5A\x15\x5A\x16\x5A\x17\x5A\x1A\x5A\x1C\x5A\x1E\x5A\x1F\xF0')

        ####### Sensors to read:
        ## [00] 0x01 RPM
        ## [01] 0x05 MAF (V)
        ## [02] 0x08 TMP COOLANT TEMP(Centigrade degrees)
        ## [03] 0x09 OXY O2 SENSOR(V)
        ## [04] 0x0B KMH
        ## [05] 0x0C BAT (V)
        ## [06] 0x0D THL THRTL POSITION(V)
        ## [07] 0x15 INJ INJECTION TIME(ms)
        ## [08] 0x16 TIM IGN TIMING(BTDC)
        ## [09] 0x17 IDL IACV - AAC / V( %)  (IDLE)
        ## [10] 0x1A AFS A/F ALPHA - LH
        ## [11] 0x1C AFL A/F ALPHA - LH(SELF - LEARN
        ## [12] 0x1E DR0 DIGITAL CONTROL REGISTER 0
        ## [13] 0x1F DR1 DIGITAL CONTROL REGISTER 1

        print('waiting for ECU to stream data...')

        while self.stream == False:
            Header = 255
            returnBytes = 14
            frameStart = self.port.read(3)
            frameList = map(ord, frameStart)

            if frameList[1] == Header and frameList[2] == returnBytes:
                print('Data stream aligned, streaming from ECU.')
                self.stream = True
            else:
                print('Aligning data stream from ECU...')

        while self.stream == True:
            incomingData = self.port.read(16)
            if incomingData:
                # We have a full line we could store into a file here

                dataList = map(ord, incomingData)
                # convertValues (dataList)
                d['RPM'] = int(round((dataList[0] * 12.5), 2))
                d['RPM'] = 500

            else:
                pass

    def convertValues(self, readvalues):
        self.integrity = False  # Until all registers have been processed, data is marked invalid

        self.D['RPM'] = int(round((readvalues[0] * 12.5), 2))
        self.D['MAF'] = readvalues[1] * 5
        self.D['TMP'] = readvalues[2] - 50
        self.D['OXY'] = readvalues[3] * 10
        self.D['KMH'] = int(round(readvalues[4] * 2))
        self.D['BAT'] = round(((readvalues[5] * 80) / 1000), 1)
        self.D['THL'] = readvalues[6] * 20
        self.D['INJ'] = readvalues[7] / 100
        self.D['TIM'] = 110 - readvalues[8]
        self.D['IDL'] = readvalues[9] / 2
        self.D['AFS'] = readvalues[10]
        self.D['AFL'] = readvalues[11]
        self.D['DR0'] = readvalues[12]
        self.D['DR1'] = readvalues[13]

        self.integrity = True
        return True

    def getIntegrity(self):
        return self.integrity

    def getData(self):
        return self.D
