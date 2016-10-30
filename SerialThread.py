#!/usr/bin/python
# SerialThread.py

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


import sys, time, math, threading, datetime
import memdata


class SerialThread(threading.Thread):
    def __init__(self, port, connected=False):
        self.port = port
        self.connected = False
        self.stream = False
        self.integrity = False

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

        #self.port.write(
        #    '\x5A\x01\x5A\x05\x5A\x08\x5A\x09\x5A\x0B\x5A\x0C\x5A\x0D\x5A\x15\x5A\x16\x5A\x17\x5A\x1A\x5A\x1C\x5A\x1E\x5A\x1F\xF0')

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
            incoming_data = self.port.read(16)
            if incoming_data:
                # We have a full line we could store into a file here

                datalist = map(ord, incoming_data)
                self.convertvalues(datalist)

            else:
                pass

    def convertvalues(self, readvalues):
        memdata.integrity = False  # Until all registers have been processed, data is marked invalid

        memdata.D['RPM'] = int((readvalues[0] * 12.5))
        memdata.D['MAF'] = readvalues[1] * 5
        memdata.D['TMP'] = readvalues[2] - 50
        memdata.D['OXY'] = readvalues[3] * 10
        memdata.D['KMH'] = readvalues[4] * 2
        memdata.D['BAT'] = round(((readvalues[5] * 80) / 1000), 1)
        memdata.D['THL'] = readvalues[6] * 20
        memdata.D['INJ'] = round((readvalues[7] / 100), 1)
        memdata.D['TIM'] = 110 - readvalues[8]
        memdata.D['IDL'] = round(readvalues[9] / 2, 1)
        memdata.D['AFS'] = readvalues[10]
        memdata.D['AFL'] = readvalues[11]
        memdata.D['DR0'] = readvalues[12]
        memdata.D['DR1'] = readvalues[13]

        memdata.integrity = True
        return True

