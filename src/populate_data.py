#! /usr/bin/env python3

import data as data
import json
import pandas as pd
import gaia

def sources():
    sources = pd.read_csv("../data/gezari_clean.csv")
    for i in range(53):
        row = sources.iloc[i].to_dict()
        info = {}
        with open('../data/sources/' + row['ID'] + '/info.json') as file:
            info = json.load(file)
        galexRA = info['NUV']['nearest_source']['skypos'][0]
        galexDE = info['NUV']['nearest_source']['skypos'][1]
        r = gaia.query(galexRA, galexDE)
        data.insert_source(row['ID'],row['RAdeg'],row['DEdeg'],galexRA,galexDE,r['source_id'][0],r['ra'][0],r['dec'][0],r['parallax'][0])

def lightcurve(sourceID):
    source = data.get_source(sourceID)
    print(source['GalexRA'])

if __name__ == '__main__':
    lightcurve('GROTH_MOS01-21')
