#! /usr/bin/env python3

import data as data
import json
import pandas as pd
# import gaia
from gPhoton import gAperture

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

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

def lightcurve(SourceID):
    source = data.get_source(SourceID)
    RA = float(source['GalexRA'])
    DE = float(source['GalexDE'])
    outFile = SourceID + '-lightcurve.csv'
    ap = data.get_parameter('ApertureRadius')
    annIn = data.get_parameter('AnnulusInnerRadius')
    annOut = data.get_parameter('AnnulusOuterRadius')
    gAperture(band='NUV', skypos=[RA,DE], stepsz=10,
        csvfile=outFile, radius=ap,
        annulus=[annIn, annOut], verbose=3)
    # data.drop_table(SourceID + '_lightcurve', True, True)
    data.refresh_connection()
    data.create_lightcurve_table(SourceID, pd.read_csv(outFile))

def all_lightcurves():
    for i in range(1,54):
        source = data.get_source(i)
        if data.get_lock_status(source['SourceID'], 'lightcurve') is None:
            data.create_lock(source['SourceID'], 'lightcurve')
            lightcurve(source['SourceID'])
            data.change_lock(source['SourceID'], 'lightcurve', 'complete')

if __name__ == '__main__':
    all_lightcurves()
    # lightcurve('GROTH_MOS01-21')
    # sources()
