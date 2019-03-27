import os
import json
import gPhoton
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def info(star):
    dir = 'data/stars/' + star['ID']
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)
    print('Fetching info for ' + star['ID'])
    info = gPhoton.gFind(band='NUV', skypos=[star['RAdeg'],star['DEdeg']])
    with open(dir + '/info.json', 'w') as fp:
        json.dump(info, fp, cls=NumpyEncoder)
    return info

def bins(star):
    infoFile = 'data/stars/' + star['ID'] + '/info.json'
    if not os.path.exists(infoFile):
        info(star)
    infoList = []
    with open(infoFile) as json_file:
        infoList = json.load(json_file)
    infoList = infoList['NUV']
    dataFile = 'data/stars/' + star['ID'] + '/bins.csv'
    print('Fetching: ' + star['ID'])
    print('Fetching bins for ' + star['ID'])
    gPhoton.gAperture(band='NUV', skypos=[star['RAdeg'],star['DEdeg']],
        csvfile=dataFile, radius=0.012,
        annulus=[0.013,0.016], verbose=2)

def window(star):
    binsFile = 'data/stars/' + star['ID'] + '/bins.csv'
    if not os.path.exists(binsFile):
        bins(star)
    binsList = pd.read_csv(binsFile)
    # print(len(bins))
    # bins = bins.loc[bins['flux_mcatbgsub']!=bins['flux_mcatbgsub'].max()]
    # print(len(bins))
    flare = binsList.loc[binsList['flux_mcatbgsub'].idxmax()]
    windowFile = 'data/stars/' + star['ID'] + '/window.csv'
    print('Fetching brightest window for ' + star['ID'])
    gPhoton.gAperture(band='NUV', skypos=[star['RAdeg'],star['DEdeg']], stepsz=10.,
        csvfile=windowFile, radius=0.012,
        annulus=[0.013,0.016], verbose=2,
        trange=[flare['t0'],flare['t1']])

def flare(star):
    print('Please delimit flare:')
    windowFile = 'data/stars/' + star['ID'] + '/window.csv'
    if not os.path.exists(windowFile):
        fetch.window(star)
    flare = pd.read_csv(windowFile)
    fig = flare.plot(x="t_mean",y="flux_mcatbgsub").get_figure()
    coords = []
    def onclick(event):
        global ix, iy
        ix, iy = event.xdata, event.ydata
        print('x = %d, y = %d'%(
            ix, iy))
        coords.append(ix)
        if len(coords) == 2:
            fig.canvas.mpl_disconnect(cid)
            plt.close(fig)
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    flareFile = 'data/stars/' + star['ID'] + '/flare.csv'
    print('Fetching flare for ' + star['ID'])
    gPhoton.gAperture(band='NUV', skypos=[star['RAdeg'],star['DEdeg']], stepsz=2.,
        csvfile=flareFile, radius=0.012,
        annulus=[0.013,0.016], verbose=2,
        trange=[round(coords[0]),round(coords[1])])
