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


def set_source_height(sourceID, height):
    try:
        query = "UPDATE TABLE Sources SET Height = %f WHERE SourceID = '%s';" % (height, sourceID)
        print(query)
        cursor.execute(query)
        db.commit()
    except Exception as e:
        print("could not set height")
        print(e)
        db.rollback()
