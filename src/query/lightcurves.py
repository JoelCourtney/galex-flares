import pandas as pd
from query.db import *


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


def get_lightcurve_fluxes(sourceID):
    try:
        query = "SELECT t0, t1, flux, flux_bgsub FROM Lightcurves WHERE SourceID = '%s' ORDER BY t0 ASC LIMIT 100000;" % sourceID
        print(query)
        df = pd.read_sql(query, db)
        return df
    except Exception as e:
        print("lightcurve query failed")
        print(e)


def get_lightcurve_range(sourceID, start, end):
    try:
        query = "SELECT * FROM Lightcurves WHERE (SourceID = '%s') AND (t0 >= %d) AND (t0 <= %d) ORDER BY t0 LIMIT 10000;" % (sourceID,start,end)
        print(query)
        df = pd.read_sql(query, db)
        return df
    except Exception as e:
        print("lightcurve range query failed")
        print(e)