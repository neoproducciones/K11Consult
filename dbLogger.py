#!/usr/bin/python
# dbLogger.py

#Copyright (C) 2016 Javier Nuevo - www.facebook.com/neoproducciones

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
import sqlite3 as db

""" Log arbitrary "two string" information to an sqlite3 database """


class LogDB:
    def __init__(self):
        self.bOpen = False

    def open(self):
        """ Connect to the LOCAL database """
        if self.bOpen == True:
            return
        self.conn = sqlite3.connect('PyLog.sqlt3')
        self.curs = self.conn.cursor()
        self.bOpen = True

    def createTable(self):
        """ Create a table for the logged messages """
        self.open()
        cmd = 'create table logged \
           (timestr char(20), message char(256))'
        self.curs.execute(cmd)
        self.close()

    def dropTable(self):
        """ Remove the table from the database """
        self.open()
        cmd = 'drop table logged'
        self.curs.execute(cmd)
        self.close()

    def insertRow(self, timestr, message):
        """ Insert an arbitrary logge prefix & message """
        self.curs.execute('insert into logged values(?,?)', [timestr, message])

    def selectMessages(self):
        """ Generator to enumerate thru selected values """
        self.curs.execute('select * from logged')
        for tstr, msg in self.curs.fetchall():
            yield tstr, msg

    def close(self):
        """ Safe coding is no accident ... """
        if self.bOpen:
            self.conn.commit()
        self.bOpen = False


if __name__ == "__main__":
    db = LogDB()
    db.createTable()
    try:
        db.open()
        for ss in range(10):
            db.insertRow("MyTime" + str(ss), "Message " + str(ss + 1))
        for zt, mgs in db.selectMessages():
            print(zt, mgs)
    finally:
        db.close()
        db.dropTable()