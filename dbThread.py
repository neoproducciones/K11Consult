#!/usr/bin/python
# dbThread.py

# Copyright (C) 2016 Javier Nuevo - www.facebook.com/neoproducciones

# TODO:   Convert into a thread

import datetime, time, math
import threading
import sqlite3
from peewee import *
import memdata



class dbThread(threading.Thread):
    class Session(Model):
        #  id = BigIntegerField(unique=True) it's automatically added by peewee
        start_time = DateTimeField()
        end_time = DateTimeField()
        closed = BooleanField()
        log_delay = IntegerField()
        last_entry = BigIntegerField()

        class Meta:
            database = db

    class DataRead(Model):
        #  id = BigIntegerField(unique=True) it's automatically added by peewee
        session_id = ForeignKeyField(Session, related_name='readings')
        entry = BigIntegerField()
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
        new_session = Session(start_time=datetime.datetime.now(), end_time='', closed=False,
                              log_delay=memdata.loguear_ms)
        new_session.save()

        #  leer ultimo registro de tabla logs - No es necesario
        #  session_id = Session.select().order_by(Session.id.desc()).get()
        return new_session.id

    def write_values(session, d, entry):
        print ("-dentro de escribe_tupla")
        #  data = DataRead (session_id=session, entry=entry, timestamp=datetime.datetime.now())
        #  We better do not record datetime due to efficiency reasons
        data = DataRead(session_id=session, entry=entry)

        data.rpm = d.RPM
        data.maf = d.MAF
        data.tmp = d.TMP
        data.oxy = d.OXY
        data.kmh = d.KMH
        data.bat = d.BAT
        data.thl = d.THL
        data.inj = d.INJ
        data.tim = d.TIM
        data.idl = d.IDL
        data.afs = d.AFS
        data.afl = d.AFL
        data.dr0 = d.DR0
        data.dr1 = d.DR1

        data.create()
        return True

    def close_session(session, entry):
        query = Session.update(end_time=datetime.datetime.now(), closed=True, last_entry=entry).where(
            Session.id == session)
        query.execute()
        return True

    def logging():
        print ("Conectando a base de datos")
        if not db.connect():
            print("Error conectando a base de datos")
            return False
        print("Base de datos conectada")
        print("Activando log")

        id_session = start_session()

        if id_session > 0:
            print("Escribiendo datos")
            entry = 0
            while memdata.loguear:
                write_values(id_session, entry, memdata.D)
                entry = entry + 1
                time.sleep(memdata.loguear_ms)
            print("Cerrando sesion")
            close_session(id_session, entry)
            print("Sesion cerrada")
        else:
            print("Error creando sesion")

    def __init__(self):
        db = SqliteDatabase('database.s3db')
        # db is the database containing all data


        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        logging()


