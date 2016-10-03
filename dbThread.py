#!/usr/bin/python
# dbThread.py

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


import datetime, time, math
import threading
import sqlite3
from peewee import *
import memdata

db = SqliteDatabase('database.s3db')
# sdb is the database containing all sessions table

class Sessions(Model):
    id = BigIntegerField(unique=True)
    start_time = DateTimeField()
    end_time = DateTimeField()
    closed = BooleanField()
    log_delay = IntegerField()
    class Meta:
        database = db # This model uses the "people.db" database.


class DataRead(Model):
    id = BigIntegerField(unique=True)
    session_id = ForeignKeyField(Sessions, related_name='readings')
    reading_num = BigIntegerField()
    timestamp = DateTimeField()
    
    class Meta:
        database = db # This model uses the "people.db" database.



def existe_tabla_logs():
    return False


def crear_tabla_logs():
    return True


def crear_sesion():
    clave = -1
    clave = 342
    return clave


def escribe_tupla (sesion, diccionario):
    print ("-dentro de escribe_tupla")
    return True


def cerrar_sesion (sesion):
    return True


def activar_log():
    print ("Conectando a base de datos")
    if not db.connect():
        print("Error conectando a base de datos")
        return False
    print("Base de datos conectada")
    print("Activando log")
    if not existe_tabla_logs():
        print("Creando tabla de logs")
        crear_tabla_logs()
    print("Creando sesion")
    id_sesion = crear_sesion()

    if id_sesion > 0:
        print("Escribiendo datos")
        while memdata.loguear:
            escribe_tupla (id_sesion, memdata.D)
            time.delay(memdata.loguear_ms)
        print("Cerrando sesion")
        cerrar_sesion(id_sesion)
        print("Sesion cerrada")
    else:
        print("Error creando sesion")
