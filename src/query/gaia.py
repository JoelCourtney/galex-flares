#! /usr/bin/env python3

import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia
import warnings
warnings.filterwarnings('ignore')


def query(RA,DE):
    coord = SkyCoord(ra=RA, dec=DE, unit=(u.degree, u.degree), frame='icrs')
    width = u.Quantity(0.1, u.deg)
    height = u.Quantity(0.1, u.deg)
    r = Gaia.query_object_sync(coordinate=coord, width=width, height=height)
    return r


def query_ids(ids):
    query = "SELECT * FROM gaiadr2.gaia_source WHERE source_id IN (%s);" % ','.join(str(i) for i in ids)
    print(query)
    job = Gaia.launch_job(query)
    r = job.get_results()
    return r