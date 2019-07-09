#! /usr/bin/env python3

import pymysql as sql
import atexit
import pandas as pd
import os


def insert_nulls(s):
    while True:
        newS = s.replace(',,',',null,').replace('inf','null')
        if newS == s:
            return newS
        else:
            s = newS


def clean_dashes(s):
    return s.replace('-', '_')


def close():
    print("Closing connection")
    db.close()


atexit.register(close)

db = sql.connect(
    'galex-flares-new.chbe8bqs2zwl.us-east-1.rds.amazonaws.com',
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


def refresh_connection():
    db = sql.connect(
        'galex-flares.chbe8bqs2zwl.us-east-1.rds.amazonaws.com',
        'joelcourtney',
        'Peri-melasma*',
        'galex_flares'
    )
    cursor = db.cursor(sql.cursors.DictCursor)


def insert_source(SourceID, GezariRA, GezariDE, GalexRA, GalexDE, GaiaID, GaiaRA, GaiaDE, Parallax):
    try:
        query = "INSERT INTO Sources (SourceID, GezariRA, GezariDE, GalexRA, GalexDE, GaiaID, GaiaRA, GaiaDE, Parallax) VALUES ('%s',%.15f,%.15f,%.15f,%.15f,%d,%.15f,%.15f,%.15f);" % (SourceID, GezariRA, GezariDE, GalexRA, GalexDE, GaiaID, GaiaRA, GaiaDE, Parallax)
        print(query)
        cursor.execute(query)
        db.commit()
    except Exception as e:
        db.rollback()
        print("insert source failed")
        print(e)


def insert_flare(SourceID, Quality, FlareStart, FlareEnd, QuiesentStart=0, QuiesentEnd=0):
    try:
        query = "INSERT INTO Flares (SourceID, Quality, FlareStart, FlareEnd, QuiesentStart, QuiesentEnd) VALUES ('%s',%s,%d,%d,%d,%d);" % (SourceID, Quality, FlareStart, FlareEnd, QuiesentStart, QuiesentEnd)
        print(query)
        cursor.execute(query)
        db.commit()
    except Exception as e:
        db.rollback()
        print("insert flare failed")
        print(e)


def get_flare(FlareID):
    try:
        query = "SELECT * FROM Flares WHERE FlareID = %d;" % FlareID
        print(query)
        cursor.execute(query)
        return cursor.fetchone()
    except Exception as e:
        print("Could not get flare")
        print(e)


def get_flares_for_source(SourceID):
    try:
        query = "SELECT * FROM Flares WHERE SourceID = '%s';" % SourceID
        print(query)
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print("could not get flares for source")
        print(e)


def get_good_flares():
    try:
        query = "SELECT * FROM Flares WHERE Quality = 1;"
        print(query)
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print("could not get all flares")
        print(e)


def delete_flares(SourceID):
    try:
        query = "DELETE FROM Flares WHERE SourceID = '%s';" % SourceID
        print(query)
        cursor.execute(query)
        db.commit()
    except Exception as e:
        db.rollback()
        print("delete flares failed")
        print(e)


def set_energy(FlareID, Energy):
    try:
        query = "UPDATE Flares SET Energy = %f WHERE FlareID = '%s';" % (Energy, FlareID)
        print(query)
        cursor.execute(query)
        db.commit()
    except Exception as e:
        db.rollback()
        print("could not set energy")
        print(e)


def get_all_energies():
    try:
        query = "SELECT Energy FROM Flares WHERE Energy IS NOT NULL;"
        print(query)
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print("could not get energies")
        print(e)


def get_source(sourceID):
    if isinstance(sourceID, str):
        try:
            query = "SELECT * FROM Sources WHERE SourceID = '%s';" % sourceID
            print(query)
            cursor.execute(query)
            return cursor.fetchone()
        except Exception as e:
            print("Source ID not found")
            print(e)
    else:
        try:
            query = "SELECT * FROM Sources WHERE RowNum = %d;" % sourceID
            print(query)
            cursor.execute(query)
            return cursor.fetchone()
        except Exception as e:
            print("RowNum not found")
            print(e)


def get_parallax(SourceID):
    if isinstance(SourceID, str):
        try:
            query = "SELECT Parallax FROM Sources WHERE SourceID = '%s';" % SourceID
            print(query)
            cursor.execute(query)
            return float(cursor.fetchone()['Parallax'])
        except Exception as e:
            print("Source ID not found")
            print(e)
    else:
        try:
            query = "SELECT Parallax FROM Sources WHERE RowNum = %d;" % SourceID
            print(query)
            cursor.execute(query)
            return float(cursor.fetchone()['Parallax'])
        except Exception as e:
            print("RowNum not found")
            print(e)


def create_lock(SourceID, Attribute):
    try:
        query = "INSERT INTO Locks (SourceID, Attribute, Status) VALUES ('%s', '%s', 'taken');" % (SourceID, Attribute)
        print(query)
        cursor.execute(query)
        db.commit()
        return True
    except Exception as e:
        print("Could not get lock: %s, %s" % (SourceID, Attribute))
        print(e)
        db.rollback()
        return False


def change_lock(SourceID, Attribute, Status):
    try:
        query = "UPDATE Locks SET Status = '%s' WHERE SourceID = '%s' AND Attribute = '%s';" % (Status, SourceID, Attribute)
        print(query)
        cursor.execute(query)
        db.commit()
    except Exception as e:
        db.rollback()
        print('Could not change lock')
        print(e)


def release_lock(SourceID, Attribute):
    try:
        query = "DELETE FROM Locks WHERE SourceID = '%s' AND Attribute = '%s';" % (SourceID, Attribute)
        print(query)
        cursor.execute(query)
        db.commit()
    except Exception as e:
        db.rollback()
        print("Could not release lock: %s, %s" % (SourceID, Attribute))
        print(e)


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
    except Exception as e:
        print("Could not check status")
        print(e)


def clear_locks():
    try:
        query = "DELETE FROM Locks WHERE Status <> 'complete';"
        print(query)
        cursor.execute(query)
        db.commit()
    except Exception as e:
        db.rollback()
        print("Could not clear locks")
        print(e)


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
    except Exception as e:
        print("Parameter not found")
        print(e)


def drop_table(table, areYouSure, areYouReallySure):
    table = clean_dashes(table)
    if areYouSure and areYouReallySure:
        try:
            query = "DROP TABLE %s" % table
            print(query)
            cursor.execute(query)
            db.commit()
        except Exception as e:
            db.rollback()
            print("Table %s doesn't exist" % table)
            print(e)


def insert_lightcurve(SourceID):
    try:
        file = '../data/lightcurves/' + SourceID + '-lightcurve.csv'
        with open(file) as curve:
            lines = curve.readlines()
            header = lines[0]
            del lines[0]
            start = "INSERT INTO Lightcurves (SourceID,%s) VALUES " % header
            query = start
            for i, line in enumerate(lines):
                line = insert_nulls(line)
                query = query + "('%s',%s)," % (SourceID, line)
                if i > 10 and i % 1000 == 0:
                    query = query[:-1] + ';'
                    # print(query)
                    cursor.execute(query)
                    query = start
            if i % 1000 != 0:
                query = query[:-1] + ';'
                # print(query)
                cursor.execute(query)
        db.commit()
    except Exception as e:
        print("could not insert lightcurve")
        print(e)
        db.rollback()
        exit()


def get_lightcurve(sourceID):
    try:
        query = "SELECT * FROM Lightcurves WHERE SourceID = '%s' ORDER BY t0 ASC LIMIT 100000;" % sourceID
        print(query)
        df = pd.read_sql(query, db)
        return df
    except Exception as e:
        print("lightcurve query failed")
        print(e)


def get_exposures(sourceID):
    expsFile = '../data/sources/' + sourceID + '/exposures.csv'
    if not os.path.exists(expsFile):
        print(sourceID + " info file does not exist")
    info = pd.read_csv(expsFile)
    exps = info[['t0', 't1', 't_mean']].copy()
    return exps


def get_lightcurve_range(sourceID, start, end):
    try:
        query = "SELECT * FROM Lightcurves WHERE (SourceID = '%s') AND (t0 >= %d) AND (t0 <= %d) ORDER BY t0 LIMIT 10000;" % (sourceID,start,end)
        print(query)
        df = pd.read_sql(query, db)
        return df
    except Exception as e:
        print("lightcurve range query failed")
        print(e)
