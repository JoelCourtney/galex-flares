#! /usr/bin/env python3

import sources as Sources
import info as Info
import json
import bright as Bright
from shutil import copyfile

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def create_info():
    knownFlares = []
    for i in range(53):
        source = Sources.get(row=i)
        contents = Info.get(source)['bright_contents']
        for n,c in enumerate(contents):
            if c == 'flare':
                print(source['ID'])
                knownFlares.append({
                    'source': source['ID'],
                    'bright_window': n
                })
    path = 'data/flares/known_flares.json'
    with open(path, 'w') as fp:
        json.dump(knownFlares, fp, cls=NumpyEncoder, indent=4)
def write_info(info):
    path = 'data/flares/known_flares.json'
    with open(path,'w') as fp:
        json.dump(info, fp, cls=NumpyEncoder, indent=4)
def read_info():
    path = 'data/flares/known_flares.json'
    with open(path) as json_file:
        flares = json.load(json_file)
        return flares

def write_times(flare_n, flare, quiesent):
    path = 'data/flares/known_flares.json'
    info = read_info()
    info[flare_n]['quiesent'] = quiesent
    info[flare_n]['flare'] = flare
    write_info(info)
