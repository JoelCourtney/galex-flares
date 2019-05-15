#! /usr/bin/env python3

import pymysql as sql
import atexit

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
    try:
        query = "SELECT * FROM Sources where SourceID = '%s';" % sourceID
        print(query)
        cursor.execute(query)
        return cursor.fetchone()
    except:
        print("Source ID not found")
