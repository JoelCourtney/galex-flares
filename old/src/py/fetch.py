import os
import json
import gPhoton
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def fetch_window(star):
    exps = read_exposures(star)
    info = read_info(star)
    for _ in range(info['flare']['reject']):
        exps = exps.loc[exps['flux_mcatbgsub']!=exps['flux_mcatbgsub'].max()]
    flare = exps.loc[exps['flux_mcatbgsub'].idxmax()]
    windowFile = 'data/stars/' + star['ID'] + '/window.csv'
    print('Fetching brightest window for ' + star['ID'])
    gPhoton.gAperture(band='NUV', skypos=info['NUV']['nearest_source']['skypos'], stepsz=30.,
        csvfile=windowFile, radius=info['aperture']['rad'],
        annulus=info['aperture']['ann'], verbose=2,
        trange=[flare['t0'],flare['t1']])
def read_window(star):
    windowFile = 'data/stars/' + star['ID'] + '/window.csv'
    if not os.path.exists(windowFile):
        fetch_window(star)
    return pd.read_csv(windowFile)

def fetch_flare(star):
    window = read_window(star)
    fig = window.plot(x="t_mean",y="flux_mcatbgsub").get_figure()
    times = []
    def onclick(event):
        global ix, iy
        ix, iy = event.xdata, event.ydata
        print('x = %d, y = %d'%(
            ix, iy))
        times.append(round(ix))
        if len(times) == 3:
            fig.canvas.mpl_disconnect(cid)
            plt.close(fig)
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    print('Please delimit flare for ' + star['ID'])
    plt.show()

    info = read_info(star)
    info['flare']['t_quiesent'] = times[0]
    info['flare']['t_start'] = times[1]
    info['flare']['t_end'] = times[2]
    write_info(star, info)

    flareFile = 'data/stars/' + star['ID'] + '/flare.csv'
    print('Fetching flare for ' + star['ID'])
    gPhoton.gAperture(band='NUV', skypos=info['NUV']['nearest_source']['skypos'], stepsz=2.,
        csvfile=flareFile, radius=info['aperture']['rad'],
        annulus=info['aperture']['ann'], verbose=2,
        trange=times[0:1])
def read_flare(star):
    flareFile = 'data/stars/' + star['ID'] + '/flare.csv'
    if not os.path.exists(flareFile):
        fetch_flare(star)
    return pd.read_csv(flareFile)
