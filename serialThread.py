#!/usr/bin/python
# serialThread.py

#Copyright (C) 2014 Eilidh Fridlington http://eilidh.fridlington.com

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


import time
import math
import threading
import datetime



class ReadStream(threading.Thread):

    def __init__(self, port,connected = False):
        self.port = port
        self.connected  = connected
        self.stream = False
        self.integrity = False

        # D es una variable global de tipo diccionario

        D['RPM'] = 0
        D['MAF'] = 0
        D['TMP'] = 0
        D['OXY'] = 0
        D['KMH'] = 0
        D['BAT'] = 0
        D['THL'] = 0
        D['INJ'] = 0
        D['TIM'] = 0
        D['IDL'] = 0
        D['AFS'] = 0
        D['AFL'] = 0
        D['DR0'] = 0
        D['DR1'] = 0

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
                    print ('Correct reply from ECU, sending data...')
                    self.connected = True

                else:
                    print ('Wrong reply from ECU')

            else:
                print ('Trying to connect to ECU')
                self.port.write('\xFF\xFF\xEF')
                time.sleep(2)


        self.port.write('\x5A\x01\x5A\x05\x5A\x08\x5A\x09\x5A\x0B\x5A\x0C\x5A\x0D\x5A\x15\x5A\x16\x5A\x17\x5A\x1A\x5A\x1C\x5A\x1E\x5A\x1F\xF0')

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

        print ('waiting for ECU to stream data...')

        while self.stream == False:
            Header = 255
            returnBytes = 14
            frameStart = self.port.read(3)
            frameList = map(ord,frameStart)

            if frameList[1] == Header and frameList[2] == returnBytes:
                print ('Data stream aligned, streaming from ECU.')
                self.stream = True
            else:
                print ('Aligning data stream from ECU...')

        while self.stream == True:
            incomingData = self.port.read(16)
            if incomingData:
                # We have a full line we could store into a file here

                dataList = map(ord,incomingData)
                #convertValues (dataList)
                D['RPM'] = int(round((dataList[0] * 12.5), 2))
                print(D['RPM'])


            else:
                pass

    def convertValues (readvalues):
        self.integrity = False  # Until all registers have been processed, data is marked invalid

        D['RPM'] = int(round((readvalues[0] * 12.5),2))
        D['MAF'] = readvalues[1] * 5
        D['TMP'] = readvalues[2] - 50
        D['OXY'] = readvalues[3] * 10
        D['KMH'] = int(round (readvalues[4] * 2))
        D['BAT'] = round(((readvalues[5] * 80) / 1000),1)
        D['THL'] = readvalues[6] * 20
        D['INJ'] = readvalues[7] / 100
        D['TIM'] = 110 - readvalues[8]
        D['IDL'] = readvalues[9] / 2
        D['AFS'] = readvalues[10]
        D['AFL'] = readvalues[11]
        D['DR0'] = readvalues[12]
        D['DR1'] = readvalues[13]

        print (D['RPM'] )

        self.integrity = True
        return true


#    def convertToKMH(self,inputData):
#        return int(round (inputData * 2))

#    def convertToRev(self,inputData):
#        return int(round((inputData * 12.5),2))

#    def convertToTemp(self,inputData):
#        return inputData - 50

#    def convertToBattery(self,inputData):
#        return round(((inputData * 80) / 1000),1)

#    def convertToMAF(self,inputData):
#       return inputData * 5

#    def convertToAAC(self,inputData):
#        return inputData / 2

#    def convertToInjection(self,inputData):
#        return inputData / 100

#    def convertToTiming(self,inputData):
#        return 110 - inputData

    def getIntegrity(self):
        return self.integrity
