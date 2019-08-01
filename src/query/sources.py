from query.db import *
import query.sdss


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


def get_all_sources():
    try:
        query = "SELECT * FROM Sources;"
        print(query)
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print("count not get all sources")
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


def set_field(sourceID, field, value):
    try:
        query = "UPDATE Sources SET %s = %.30f WHERE SourceID = '%s';" % (field, value, sourceID)
        print(query)
        cursor.execute(query)
        db.commit()
    except Exception as e:
        print("could not set %s" % field)
        print(e)
        db.rollback()


def get_distance(SourceID): # IN PARSECS
    if isinstance(SourceID, str):
        try:
            query = "SELECT Distance FROM Sources WHERE SourceID = '%s';" % SourceID
            print(query)
            cursor.execute(query)
            return float(cursor.fetchone()['Distance'])
        except Exception as e:
            print("Source ID not found")
            print(e)
            return float('nan')
    else:
        try:
            query = "SELECT Distance FROM Sources WHERE RowNum = %d;" % SourceID
            print(query)
            cursor.execute(query)
            return float(cursor.fetchone()['Distance'])
        except Exception as e:
            print("RowNum not found")
            print(e)
            return float('nan')