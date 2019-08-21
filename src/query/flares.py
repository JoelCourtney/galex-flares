from query.db import *


def insert_flare(SourceID, Quality, FlareStart, FlareEnd, QuiesentStart=0, QuiesentEnd=0):
    execute("INSERT INTO Flares (SourceID, Quality, FlareStart, FlareEnd, QuiesentStart, QuiesentEnd) VALUES ('%s',%s,%d,%d,%d,%d);" % (SourceID, Quality, FlareStart, FlareEnd, QuiesentStart, QuiesentEnd))


def get_flare(FlareID):
    return fetch_one("SELECT * FROM Flares WHERE FlareID = %d;" % FlareID)


def get_flares_for_source(SourceID):
    return fetch_all("SELECT * FROM Flares WHERE SourceID = '%s';" % SourceID)


def get_good_flares_for_source(SourceID):
    return fetch_all("SELECT * FROM Flares WHERE Quality = TRUE AND SourceID = '%s';" % SourceID)


def get_good_flares():
    return fetch_all("SELECT * FROM Flares WHERE Quality = 1;")


def delete_flares(SourceID):
    execute("DELETE FROM Flares WHERE SourceID = '%s';" % SourceID)


def set_energy(FlareID, Energy):
    execute("UPDATE Flares SET Energy = %f WHERE FlareID = '%s';" % (Energy, FlareID))


def get_all_energies():
    return fetch_all("SELECT Energy FROM Flares WHERE Energy IS NOT NULL;")
