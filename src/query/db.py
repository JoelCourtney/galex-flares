import pymysql as sql
import atexit
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
    'MdNrd2zN$4p3!nGzb2%wctMTKXzKs*RSKiKzEnb%E8p@UyAD$',
    'galex_flares'
)
# prepare a cursor object using cursor() method
cursor = db.cursor(sql.cursors.DictCursor)

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Database version : %s " % data)


def refresh_connection():
    db = sql.connect(
        'galex-flares.chbe8bqs2zwl.us-east-1.rds.amazonaws.com',
        'joelcourtney',
        'MdNrd2zN$4p3!nGzb2%wctMTKXzKs*RSKiKzEnb%E8p@UyAD$',
        'galex_flares'
    )
    cursor = db.cursor(sql.cursors.DictCursor)










