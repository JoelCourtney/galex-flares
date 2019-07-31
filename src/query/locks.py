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