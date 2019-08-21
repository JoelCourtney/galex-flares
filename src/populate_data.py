#! /usr/bin/env python3

import json
import pandas as pd
from gPhoton import gAperture
import os
import math
import query.gaia
import query.sources
import query.lightcurves
import query.misc
import query.spectra
import numpy as np
from shutil import copyfile
from astropy.io import fits


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
        r = query.gaia.query(galexRA, galexDE)
        query.sources.insert_source(row['ID'], row['RAdeg'], row['DEdeg'], galexRA, galexDE, r['source_id'][0],
                                    r['ra'][0], r['dec'][0], r['parallax'][0])


def lightcurve(SourceID):
    source = query.sources.get_source(SourceID)
    ra = float(source['GalexRA'])
    de = float(source['GalexDE'])
    out_file = '../data/lightcurves/' + SourceID + '-lightcurve.csv'
    ap = query.misc.get_parameter('ApertureRadius')
    ann_in = query.misc.get_parameter('AnnulusInnerRadius')
    ann_out = query.misc.get_parameter('AnnulusOuterRadius')
    gAperture(band='NUV', skypos=[ra, de], stepsz=10,
              csvfile=out_file, radius=ap,
              annulus=[ann_in, ann_out], verbose=3)
    # data.drop_table(SourceID + '_lightcurve', True, True)
    # data.refresh_connection()
    # data.create_lightcurve_table(SourceID, pd.read_csv(out_file))


def incremental_lightcurve(sourceID):
    source = query.sources.get_source(sourceID)
    ra = float(source['GalexRA'])
    de = float(source['GalexDE'])
    ap = query.misc.get_parameter('ApertureRadius')
    ann_in = query.misc.get_parameter('AnnulusInnerRadius')
    ann_out = query.misc.get_parameter('AnnulusOuterRadius')
    dir_path = '../data/lightcurves/' + sourceID
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    start = len(os.listdir(dir_path))
    exps = query.misc.get_exposures(sourceID)
    for i in range(start, len(exps)):
        exp = exps.iloc[i]
        out_file = dir_path + '/exposure-' + str(i) + '.csv'
        gAperture(band='NUV', skypos=[ra, de], stepsz=10, trange=[exp['t0'], exp['t1']],
                  csvfile=out_file, radius=ap,
                  annulus=[ann_in, ann_out], verbose=3)


def all_lightcurves():
    for i in range(1, 54):
        source = query.sources.get_source(i)
        if query.locks.get_lock_status(source['SourceID'], 'lightcurve') is None:
            query.locks.create_lock(source['SourceID'], 'lightcurve')
            lightcurve(source['SourceID'])
            query.locks.change_lock(source['SourceID'], 'lightcurve', 'complete')


def lightcurve_table():
    for i in range(1, 54):
        source = query.sources.get_source(i)
        file = '../data/lightcurves/' + source['SourceID'] + '-lightcurve.csv'
        if os.path.exists(file):
            query.lightcurves.insert_lightcurve(source['SourceID'])


def extra_source_data():
    def calc_mag(app_mag, par):
        return app_mag + 5 * (1+math.log10(par/1000.))
    for i in range(1, 54):
        source = query.sources.get_source(i)
        gaia_obj = query.gaia.query_id(source['GaiaID'])[0]
        app_mag = gaia_obj['phot_g_mean_mag']
        color = gaia_obj['bp_rp']
        query.sources.set_field(source['SourceID'], 'AppMag', app_mag)
        query.sources.set_field(source['SourceID'], 'Color', color)
        lc = query.lightcurves.get_lightcurve(source['SourceID'])
        sd = np.std(lc[['flux']])['flux']
        mn = np.mean(lc[['flux']])['flux']
        query.sources.set_field(source['SourceID'], 'FluxMean', mn)
        query.sources.set_field(source['SourceID'], 'FluxSD', sd)
        parallax = source['Parallax']
        if parallax is not None:
            dist = 1000.0 / float(parallax)
            height = math.sin(math.radians(float(source['GalexDE']))) * dist
            query.sources.set_field(source['SourceID'], 'Distance', dist)
            query.sources.set_field(source['SourceID'], 'Height', height)
            abs_mag = calc_mag(app_mag, float(parallax))
            query.sources.set_field(source['SourceID'], 'AbsMag', abs_mag)


def combine_increments(sourceID):
    dir_path = '../data/lightcurves/' + sourceID
    dest_path = '../data/lightcurves/' + sourceID + '-lightcurve.csv'
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    num = len(os.listdir(dir_path))
    copyfile(dir_path + '/exposure-0.csv', dest_path)
    f = open(dest_path, "a+")
    for i in range(1, num):
        text = [6]
        try:
            l = open(dir_path + '/exposure-' + str(i) + '.csv', 'r')
            text = l.readlines()
            l.close()
        except:
            pass
        text.pop(0)
        for line in text:
            f.write(line)
    f.close()


def spectra():
    query.spectra.clear_spectra()
    for folder in ['n1', 'n2']:
        full_folder = '../data/iraf/' + folder + '/final/'
        for file in os.listdir(full_folder):
            parts = file.split('.')
            sourceName = parts[0]
            sourceID = query.sources.get_source(sourceName)['SourceID']
            frameID = int(parts[1][0:4])
            path = full_folder + file
            hdulist = fits.open(path)
            hdu = hdulist[0]
            shift = hdu.header['CRVAL1']
            disp = hdu.header['CD1_1']
            fluxes = hdu.data[0][0]
            length = len(fluxes)
            wavelengths = np.linspace(shift, shift + disp*(length-1), length)
            query.spectra.insert_spectra(sourceID, frameID, wavelengths, fluxes)


if __name__ == '__main__':
    spectra()
