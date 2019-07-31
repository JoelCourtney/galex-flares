from query.db import *


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


def get_good_flares_for_source(SourceID):
    try:
        query = "SELECT * FROM Flares WHERE Quality = TRUE AND SourceID = '%s';" % SourceID
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