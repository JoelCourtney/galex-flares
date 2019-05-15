import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import sys
import time
import sources as Sources
from gPhoton import gFind
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def query(source):
    print('Fetching info for ' + source['ID'])
    lock(source, 'info')
    info = gFind(band='both',
        skypos=[source['RAdeg'],source['DEdeg']],
        exponly=True, verbose=2)
    info['flares'] = {
        'num': 0,
        'bad': [],
        'times': []
    }
    info['aperture'] = {
        'rad': 0.0045,
        'ann': [0.005,0.006]
    }
    info['locks'] = []
    write_info(source, info)
    unlock(source, 'info')

def get(source):
    infoFile = 'data/sources/' + source['ID'] + '/info.json'
    if not os.path.exists(infoFile):
        write(source, {'locks': []})
        query(source)
    with open(infoFile) as json_file:
        info = json.load(json_file)
        return info

def write(source, info):
    dir = 'data/sources/' + source['ID']
    if not os.path.exists(dir):
        os.mkdir(dir)
    with open(dir + '/info.json', 'w') as fp:
        json.dump(info, fp, cls=NumpyEncoder, indent=4)

def lock(source, aspect):
    infoFile = 'data/sources/' + source['ID'] + '/info.json'
    if not os.path.exists(infoFile):
        write(source, {'locks': []})
    info = get(source)
    if aspect in info['locks']:
        return False
    else:
        info['locks'].append(aspect)
        write(source, info)
        return True

def unlock(source, aspect):
    info = get(source)
    if aspect in info['locks']:
        info['locks'].remove(aspect)
    write(source, info)

def main():
    if len(sys.argv) == 1:
        sources = Sources.all()
        for i in range(53):
            source = sources.iloc[i].to_dict()
            get(source)
    elif sys.argv[1] == 'backward':
        sources = Sources.all()
        for i in reversed(range(53)):
            source = sources.iloc[i].to_dict()
            get(source)
    else:
        for name in sys.argv[1:]:
            source = Sources.get(name)
            get(source)

if __name__ == '__main__':
    main()
