#! /usr/bin/env

from gPhoton import gMap
import bright as Bright
import sources as Sources
import info as Info

def main():
    source = Sources.get('GROTH_MOS05-15')
    info = Info.get(source)
    imageFile = 'data/sources/' + source['ID'] + '/image.fits'
    exp = Bright.get_bright_exposure(source, 4)
    gMap(band='NUV', skypos = info['NUV']['nearest_source']['skypos'],
            intensity='imageFile', angle=info['aperture']['rad'],
            trange=[exp['t0'],exp['t0']+10], verbose=2)
if __name__ == '__main__':
    main()
