from query.db import *


def get_sdss(sourceID):
    try:
        query = "SELECT * FROM SDSS WHERE SourceID = '%s';" % sourceID
        print(query)
        cursor.execute(query)
        return cursor.fetchone()
    except Exception as e:
        print("could not get sdss")
        print(e)