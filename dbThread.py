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
# db is the database containing all data


class Session(Model):
    id = BigIntegerField(unique=True)
    start_time = DateTimeField()
    end_time = DateTimeField()
    closed = BooleanField()
    log_delay = IntegerField()

    class Meta:
        database = db


class DataRead(Model):
    id = BigIntegerField(unique=True)
    session_id = ForeignKeyField(Session, related_name='readings')
    reading_num = BigIntegerField()
    timestamp = DateTimeField()

    rpm = SmallIntegerField()
    maf = SmallIntegerField()
    tmp = SmallIntegerField()
    oxy = SmallIntegerField()
    kmh = SmallIntegerField()
    bat = FloatField()
    thl = SmallIntegerField()
    inj = FloatField()
    tim = SmallIntegerField()
    idl = FloatField()
    afs = SmallIntegerField()
    afl = SmallIntegerField()
    dr0 = SmallIntegerField()
    dr1 = SmallIntegerField()

    class Meta:
        database = db




def start_session():
    db.create_tables([Session, DataRead], safe=True)  # Solo crea las tablas si no existen
    #  añadir entrada en tabla logs (el id se autoincrementa)
    new_session = Session(id=1, start_time='2016-10-10', end_time='', closed=False, log_delay=memdata.loguear_ms)

    id = BigIntegerField(unique=True)
    start_time = DateTimeField()
    end_time = DateTimeField()
    closed = BooleanField()
    log_delay = IntegerField()


    new_session.save()

    #  leer ultimo registro de tabla logs
    session_id = Session.select().order_by(Session.id.desc()).get()
    clave = -1
    clave = 342
    return session_id


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

    id_session = start_session()

    if id_session > 0:
        print("Escribiendo datos")
        while memdata.loguear:
            escribe_tupla (id_session, memdata.D)
            time.delay(memdata.loguear_ms)
        print("Cerrando sesion")
        cerrar_sesion(id_session)
        print("Sesion cerrada")
    else:
        print("Error creando sesion")
