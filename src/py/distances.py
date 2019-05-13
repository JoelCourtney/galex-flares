#! /usr/bin/env python3

import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia
import numpy as np
import info as Info
import sources as Sources

def get(source):
    info = Info.get(source)
    if 'distance' in info.keys():
        return info['distance']
    else:
        query(source)
        return get(source)

def query(source):
    info = Info.get(source)
    coord = SkyCoord(ra=info['NUV']['nearest_source']['skypos'][0], dec=info['NUV']['nearest_source']['skypos'][1], unit=(u.degree, u.degree), frame='icrs')
    width = u.Quantity(0.1, u.deg)
    height = u.Quantity(0.1, u.deg)
    r = Gaia.query_object_async(coordinate=coord, width=width, height=height)
    distance = 1000/r['parallax'][0]
    info['distance'] = distance
    Info.write(source, info)
    return distance
