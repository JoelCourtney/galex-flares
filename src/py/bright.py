from gPhoton import gAperture
import info as Info
import exposures as Exposures
import os
import sources as Sources
import pandas as pd

def get(source, n):
    brightFile = 'data/sources/' + source['ID'] + '/bright-' + str(n) + '.csv'
    if not os.path.exists(brightFile) and not query(source, n):
        return None
    return pd.read_csv(brightFile)

def query(source, n):
    if Info.lock(source, 'bright-' + str(n)):
        brightFile = 'data/sources/' + source['ID'] + '/bright-' + str(n) + '.csv'
        photonsFile = 'data/sources/' + source['ID'] + '/photons-' + str(n) + '.csv'
        info = Info.get(source)
        exp = get_bright_exposure(source, n)
        step = 10. if (exp['t1'] - exp['t0']) > 200 else 5.
        print('Querying bright exposure ' + str(n) + ' for ' + source['ID'])
        gAperture(band='NUV', skypos=info['NUV']['nearest_source']['skypos'], stepsz=step,
            csvfile=brightFile, radius=info['aperture']['rad'],
            annulus=info['aperture']['ann'], verbose=2,
            trange=[exp['t0'],exp['t1']])
        Info.unlock(source, 'bright-' + str(n))
        return True
    else:
        return False

def get_bright_exposure(source, n):
    return Exposures.get(source) \
        .sort_values(by='flux_bgsub', ascending=False) \
        .head(5).sort_values(by='t0') \
        .iloc[n].to_dict()

def main():
    for i in range(53):
        source = Sources.get(row=i)
        info = Info.get(source)
        for f in range(5):
            get(source, f)

if __name__ == '__main__':
    main()
