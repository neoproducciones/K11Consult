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
        self.integrity = False # Comprobación de integridad: todas las variables deben haber sido actualizadas
        self.KMH_Value = 0
        self.RPM_Value = 0
        self.TEMP_Value = 0
        self.BATT_Value = 0
        self.MAF_Value = 0
        self.AAC_Value = 0
        self.INJ_Value = 0
        self.TIM_Value = 0
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
                    print 'Correct reply from ECU, sending data...'
                    self.connected = True

                else:
                    print 'Wrong reply from ECU'

            else:
                print 'Trying to connect to ECU'
                self.port.write('\xFF\xFF\xEF')
                time.sleep(2)


        self.port.write('\x5A\x01\x5A\x05\x5A\x08\x5A\x09\x5A\x0b\x5A\x0c\x5A\x0d\x5A\x15\x5A\x16\x5A\x17\x5A\x1a\x5A\x1c\x5A\x1f\x5A\x23\xF0')

        ####### Sensors to read:
        ## [00] 0x01 RPM
        ## [01] 0x05 MAF(V)
        ## [02] 0x08 COOLANT TEMP(ºC)
        ## [03] 0x09 O2 SENSOR(V)
        ## [04] 0x0b KMH
        ## [05] 0x0c BATT(V)
        ## [06] 0x0d THRTL POSITION(V)
        ## [07] 0x15 INJECTION TIME(ms)
        ## [08] 0x16 IGN TIMING(BTDC)
        ## [09] 0x17 IACV - AAC / V( %)
        ## [10] 0x1a A/F ALPHA - LH
        ## [11] 0x1c A/F ALPHA - LH(SELF - LEARN)
        ## [12] 0x1f DIGITAL CONTROL REGISTER
        ## [13] 0x23 INJECTOR TIME RH -- !!! maybe not in sr20de

        print 'waiting for ECU to stream data...'

        while self.stream == False:
            Header = 255
            returnBytes = 14
            frameStart = self.port.read(3)
            frameList = map(ord,frameStart)

            if frameList[1] == Header and frameList[2] == returnBytes:
                print 'Data stream aligned, streaming from ECU.'
                self.stream = True

            else:
                print 'Aligning data stream from ECU...'

        while self.stream == True:
            incomingData = self.port.read(16)
            if incomingData:
                # We have a full line we could store into a file here

                dataList = map(ord,incomingData)
                integrity = False # Until all registers have been processed, data is marked invalid

                self.KMH_Value = self.convertToKMH(int(dataList[0]))
                self.RPM_Value = self.convertToRev(int(dataList[1]))
                self.TEMP_Value = self.convertToTemp(int(dataList[2]))
                self.BATT_Value = self.convertToBattery(float(dataList[3]))
                self.AAC_Value = self.convertToAAC(int(dataList[10]))
                self.MAF_Value = self.convertToMAF(int(dataList[7]))

                integrity = True

            else:
                pass


    def convertToKMH(self,inputData):

        return int(round (inputData * 2))

    def convertToRev(self,inputData):

        return int(round((inputData * 12.5),2))

    def convertToTemp(self,inputData):

        return inputData - 50

    def convertToBattery(self,inputData):

        return round(((inputData * 80) / 1000),1)

    def convertToMAF(self,inputData):

        return inputData * 5

    def convertToAAC(self,inputData):

        return inputData / 2

    def convertToInjection(self,inputData):

        return inputData / 100

    def convertToTiming(self,inputData):

        return 110 - inputData


    def returnMPH(self):
        return self.MPH_Value

    def returnRPM(self):
        return self.RPM_Value

    def returnTEMP(self):
        return self.TEMP_Value

    def returnBATT(self):
        return self.BATT_Value

    def returnAAC(self):
        return self.AAC_Value

    def returnMAF(self):
        return self.MAF_Value
