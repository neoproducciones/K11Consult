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
    #  id = BigIntegerField(unique=True) it's automatically added by peewee
    start_time = DateTimeField()
    end_time = DateTimeField()
    closed = BooleanField()
    log_delay = IntegerField()

    class Meta:
        database = db


class DataRead(Model):
    #  id = BigIntegerField(unique=True) it's automatically added by peewee
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
    #  add entry to logs table (self incremental id)
    new_session = Session(start_time=datetime.datetime.now(), end_time='', closed=False, log_delay=memdata.loguear_ms)
    new_session.save()

    #  leer ultimo registro de tabla logs - No es necesario
    #  session_id = Session.select().order_by(Session.id.desc()).get()
    return new_session.id


def escribe_tupla (sesion, diccionario):
    print ("-dentro de escribe_tupla")
    return True


def cerrar_sesion (sesion):
    query = Session.update(end_time=datetime.datetime.now(), closed=True).where(Session.id == sesion)
    query.execute()
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
