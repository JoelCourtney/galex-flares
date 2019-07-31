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


def get_exposures(sourceID):
    expsFile = '../data/sources/' + sourceID + '/exposures.csv'
    if not os.path.exists(expsFile):
        print(sourceID + " info file does not exist")
    info = pd.read_csv(expsFile)
    exps = info[['t0', 't1', 't_mean']].copy()
    return exps