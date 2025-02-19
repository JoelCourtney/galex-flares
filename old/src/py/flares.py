#! /usr/bin/env python3

import sources as Sources
import info as Info
import json
import bright as Bright
from shutil import copyfile
import numpy as np
import distances as Dist
import math
import matplotlib.pyplot as plt

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def get(flare_n):
    flares = read_info()
    return flares[flare_n]

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
    path = 'data/known_flares.json'
    with open(path, 'w') as fp:
        json.dump(knownFlares, fp, cls=NumpyEncoder, indent=4)
def write_info(info):
    path = 'data/known_flares.json'
    with open(path,'w') as fp:
        json.dump(info, fp, cls=NumpyEncoder, indent=4)
def read_info():
    path = 'data/known_flares.json'
    with open(path) as json_file:
        flares = json.load(json_file)
        return flares

def write_times(flare_n, flare_t, quiesent_t):
    path = 'data/known_flares.json'
    info = read_info()
    info[flare_n]['quiesent'] = quiesent_t
    info[flare_n]['flare'] = flare_t
    write_info(info)

def get_energy(flare_n):
    flares = read_info()
    if 'energy' in flares[flare_n].keys():
        return flares[flare_n]['energy']
    else:
        energy = calculate_energy(flare_n)
        flares[flare_n]['energy'] = energy
        write_info(flares)

def extract_quiesent_region(flare_n):
    flare_info = get(flare_n)
    source = Sources.get(flare_info['source'])
    flare = Bright.get(source,flare_info['bright_window'])
    return flare.loc[(flare_info['quiesent'][0] <= flare['t0']) & (flare['t0'] <= flare_info['quiesent'][1])]
def extract_flare_region(flare_n):
    flare_info = get(flare_n)
    source = Sources.get(flare_info['source'])
    flare = Bright.get(source,flare_info['bright_window'])
    return flare.loc[(flare_info['flare'][0] <= flare['t0']) & (flare['t0'] <= flare_info['flare'][1])]
def calculate_quiesent_mean(flare_n,col):
    quiesent = extract_quiesent_region(flare_n)
    return quiesent.mean(axis=0)[col]

def integrate_flux(flare_n):
    base = calculate_quiesent_mean(flare_n, 'flux_mcatbgsub')
    flare_info = get(flare_n)
    source = Sources.get(flare_info['source'])
    flare = extract_flare_region(flare_n)
    area = np.trapz(flare['flux_mcatbgsub']-base, x=flare['t0'])
    return area

def calculate_energy(flare_n):
    flare_info = read_info()[flare_n]
    source = Sources.get(flare_info['source'])
    int_flux = integrate_flux(flare_n)
    distance = Dist.get(source)
    if not distance:
        return None
    distance *= 3.086e18
    bandwidth = 950 # angstroms
    energy = int_flux * 4 * math.pi * distance**2 * bandwidth
    return energy

energies = []
for i in range(31):
    energy = calculate_energy(i)
    print(energy)
    if energy and not math.isnan(energy):
        energies.append(energy)

print(np.mean(energies))
plt.hist(energies, bins=np.logspace(30,35, 20))
plt.gca().set_xscale('log')
plt.xlabel('NUV Energy of Flare (ergs)')
plt.ylabel('# Occurances')
plt.title('Energy Distribution of Flares')
plt.show()
