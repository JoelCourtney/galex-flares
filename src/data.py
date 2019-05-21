#! /usr/bin/env python3

import pymysql as sql
import atexit
import pandas as pd

def insert_nulls(s):
    while True:
        newS = s.replace(',,',',null,')
        if newS == s:
            return newS
        else:
            s = newS
def clean_dashes(s):
    return s.replace('-','_')

def close():
    print("Closing connection")
    db.close()
atexit.register(close)

db = sql.connect(
    'galex-flares.chbe8bqs2zwl.us-east-1.rds.amazonaws.com',
    'joelcourtney',
    'Peri-melasma*',
    'galex_flares'
)
# prepare a cursor object using cursor() method
cursor = db.cursor(sql.cursors.DictCursor)

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print ("Database version : %s " % data)

def insert_source(SourceID, GezariRA, GezariDE, GalexRA, GalexDE, GaiaID, GaiaRA, GaiaDE, Parallax):
    try:
        query = "INSERT INTO Sources (SourceID, GezariRA, GezariDE, GalexRA, GalexDE, GaiaID, GaiaRA, GaiaDE, Parallax) VALUES ('%s',%.15f,%.15f,%.15f,%.15f,%d,%.15f,%.15f,%.15f);" % (SourceID, GezariRA, GezariDE, GalexRA, GalexDE, GaiaID, GaiaRA, GaiaDE, Parallax)
        print(query)
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()
        print("insert source failed")


def insert_flare(SourceID, FlareStart, FlareEnd, QuiesentStart, QuiesentEnd):
    try:
        query = "INSERT INTO Flares (SourceID, FlareStart, FlareEnd, QuiesentStart, QuiesentEnd) VALUES ('%s',%d,%d,%d,%d);" % (SourceID, FlareStart, FlareEnd, QuiesentStart, QuiesentEnd)
        print(query)
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()
        print("insert flare failed")

def get_source(sourceID):
    if isinstance(sourceID, str):
        try:
            query = "SELECT * FROM Sources WHERE SourceID = '%s';" % sourceID
            print(query)
            cursor.execute(query)
            return cursor.fetchone()
        except:
            print("Source ID not found")
    else:
        try:
            query = "SELECT * FROM Sources WHERE RowNum = %d;" % sourceID
            print(query)
            cursor.execute(query)
            return cursor.fetchone()
        except:
            print("RowNum not found")

def create_lock(SourceID, Attribute):
    try:
        query = "INSERT INTO Locks (SourceID, Attribute, Status) VALUES ('%s', '%s', 'taken');" % (SourceID, Attribute)
        print(query)
        cursor.execute(query)
        db.commit()
        return True
    except:
        print("Could not get lock: %s, %s" % (SourceID, Attribute))
        db.rollback()
        return False

def change_lock(SourceID, Attribute, Status):
    try:
        query = "UPDATE Locks SET Status = '%s' WHERE SourceID = '%s' AND Attribute = '%s';" % (Status, SourceID, Attribute)
        print(query)
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()
        print('Could not change lock')

def release_lock(SourceID, Attribute):
    try:
        query = "DELETE FROM Locks WHERE SourceID = '%s' AND Attribute = '%s';" % (SourceID, Attribute)
        print(query)
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()
        print("Could not release lock: %s, %s" % (SourceID, Attribute))

def get_lock_status(SourceID, Attribute):
    try:
        query = "SELECT Status FROM Locks WHERE SourceID = '%s' AND Attribute = '%s';" % (SourceID, Attribute)
        print(query)
        cursor.execute(query)
        res = cursor.fetchone()
        if res is not None:
            return res['Status']
        else:
            return None
    except:
        print("Could not check status")

def clear_locks():
    try:
        query = "DELETE FROM Locks WHERE Status <> 'complete';"
        print(query)
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()
        print("Could not clear locks")

def get_first_open_lock(Attribute):
    for i in range(1,54):
        source = get_source(i)
        if get_lock_status(source['SourceID'], Attribute) is None:
            return source
    return False

def get_parameter(Parameter):
    try:
        query = "SELECT Val FROM Parameters WHERE Parameter = '%s';" % Parameter
        print(query)
        cursor.execute(query)
        return float(cursor.fetchone()['Val'])
    except:
        print("Parameter not found")

def drop_table(table, areYouSure, areYouReallySure):
    table = clean_dashes(table)
    if areYouSure and areYouReallySure:
        try:
            query = "DROP TABLE %s" % table
            print(query)
            cursor.execute(query)
            db.commit()
        except:
            db.rollback()
            print("Table %s doesn't exist" % table)

def create_lightcurve_table(SourceID, file):
    SourceID = clean_dashes(SourceID)
    drop_table(SourceID+'_lightcurve', True, True)
    try:
        query = (
            "CREATE TABLE %s_lightcurve ("
            "t0 DEC(15,5),"
            "t1 DEC(15,5),"
            "t_mean DEC(15,5),"
            "t0_data DEC(15,5),"
            "t1_data DEC(15,5),"
            "cps_bgsub FLOAT(24),"
            "cps_bgsub_err FLOAT(24),"
            "flux_bgsub FLOAT(24),"
            "flux_bgsub_err FLOAT(24),"
            "mag_bgsub FLOAT(24),"
            "mag_bgsub_err_1 FLOAT(24),"
            "mag_bgsub_err_2 FLOAT(24),"
            "cps_mcatbgsub FLOAT(24),"
            "cps_mcatbgsub_err FLOAT(24),"
            "flux_mcatbgsub FLOAT(24),"
            "flux_mcatbgsub_err FLOAT(24),"
            "mag_mcatbgsub FLOAT(24),"
            "mag_mcatbgsub_err_1 FLOAT(24),"
            "mag_mcatbgsub_err_2 FLOAT(24),"
            "cps FLOAT(24),"
            "cps_err FLOAT(24),"
            "flux FLOAT(24),"
            "flux_err FLOAT(24),"
            "mag FLOAT(24),"
            "mag_err_1 FLOAT(24),"
            "mag_err_2 FLOAT(24),"
            "counts INT,"
            "flat_counts FLOAT(24),"
            "bg_counts INT,"
            "bg_flat_counts FLOAT(24),"
            "exptime FLOAT(24),"
            "bg FLOAT(24),"
            "mcat_bg FLOAT(24),"
            "responses FLOAT(24),"
            "detxs FLOAT(24),"
            "detys FLOAT(24),"
            "detrad FLOAT(24),"
            "racent FLOAT(24),"
            "deccent FLOAT(24),"
            "q_mean FLOAT(24),"
            "flags INT,"
            "PRIMARY KEY (t0)"
            ");"
        ) % SourceID
        print(query)
        cursor.execute(query)
        with open(file) as curve:
            lines = curve.readlines()
            header = lines[0]
            lines.pop(0)
            query = "INSERT INTO %s_lightcurve (%s) VALUES " % (SourceID,header)
            for line in lines:
                line = insert_nulls(line)
                query = query + "(%s)," % line
            query = query[:-1] + ';'
            # print(query)
            cursor.execute(query)
        db.commit()
    except:
        db.rollback()
        print("Failed to create table")
