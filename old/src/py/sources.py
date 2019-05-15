import pandas as pd

sources_global = pd.DataFrame()

def all():
    global sources_global
    if sources_global.empty:
        sources_global = pd.read_csv("data/gezari_clean.csv")
        sources_global['name'] = sources_global['ID']
        sources_global.set_index('name', inplace=True)
        return sources_global
    else:
        return sources_global

def get(name='', row=-1):
    sources = all()
    if name != '':
        return sources.loc[name].to_dict()
    else:
        return sources.iloc[row].to_dict()
