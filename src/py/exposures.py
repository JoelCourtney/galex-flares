import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import sys
import time
import info as Info
import sources as Sources
from gPhoton import gAperture

def query(source):
    info = Info.get(source)
    expsFile = 'data/sources/' + source['ID'] + '/exposures.csv'
    if Info.lock(source, 'exposures'):
        print('Querying exposures for ' + source['ID'])
        gAperture(band='NUV', skypos=info['NUV']['nearest_source']['skypos'],
            csvfile=expsFile, radius=info['aperture']['rad'],
            annulus=info['aperture']['ann'], verbose=2)
        Info.unlock(source, 'exposures')
        return True
    else:
        return False
def get(source):
    expsFile = 'data/sources/' + source['ID'] + '/exposures.csv'
    if not os.path.exists(expsFile) and not query(source):
            return None
    return pd.read_csv(expsFile)

def main():
    if len(sys.argv) == 1:
        for i in range(53):
            source = Sources.get(row=i)
            get(source)
    elif sys.argv[1] == 'backward':
        for i in reversed(range(53)):
            source = Sources.get(row=i)
            get(source)
    else:
        for name in sys.argv[1:]:
            source = Sources.get(name)
            get(source)

if __name__ == '__main__':
    main()
