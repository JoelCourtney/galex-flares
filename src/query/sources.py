from query.db import *
import query.sdss


def insert_source(SourceName, GezariRA, GezariDE, GalexRA, GalexDE, GaiaID, GaiaRA, GaiaDE, Parallax):
    execute("INSERT INTO Sources (SourceName, GezariRA, GezariDE, GalexRA, GalexDE, GaiaID, GaiaRA, GaiaDE, Parallax) VALUES ('%s',%.15f,%.15f,%.15f,%.15f,%d,%.15f,%.15f,%.15f);" % (SourceName, GezariRA, GezariDE, GalexRA, GalexDE, GaiaID, GaiaRA, GaiaDE, Parallax))


def get_source(sourceID):
    if isinstance(sourceID, str):
        return fetch_one("SELECT * FROM Sources WHERE SourceName = '%s';" % sourceID)
    else:
        return fetch_one("SELECT * FROM Sources WHERE SourceID = %d;" % sourceID)


def get_all_sources():
    return fetch_all('SELECT * FROM Sources;')


def get_parallax(SourceID):
    if isinstance(SourceID, str):
        return float(fetch_one("SELECT Parallax FROM Sources WHERE SourceID = '%s';" % SourceID)['Parallax'])
    else:
        return float(fetch_one("SELECT Parallax FROM Sources WHERE RowNum = %d;" % SourceID)['Parallax'])


def set_field(sourceID, field, value):
    execute("UPDATE Sources SET %s = %.30f WHERE SourceID = '%s';" % (field, value, sourceID))


def get_distance(SourceID):
    if isinstance(SourceID, str):
        return float(fetch_one("SELECT Distance FROM Sources WHERE SourceID = '%s';" % SourceID)['Distance'])
    else:
        return float(fetch_one("SELECT Distance FROM Sources WHERE RowNum = %d;" % SourceID)['Distance'])


def get_ids():
    return fetch_all("SELECT SourceID FROM Sources;")
