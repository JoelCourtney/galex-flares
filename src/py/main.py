import gPhoton
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import json
import fetch
import sys
import time

def plotFlare(star, cropped):
    flare = 0;
    if cropped:
        flare = fetch.read_flare(star)
    else:
        flare = fetch.read_window(star)
    flare.plot(x="t0",y="flux_mcatbgsub")
    plt.show()

def main():
    stars = pd.read_csv("data/gezari_clean.csv")
    for i in range(53):
        star = stars.iloc[i].to_dict()
        fetch.read_info(star)
        fetch.read_exposures(star)
        plotFlare(star, False)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    elif sys.argv[1] == 'info':
        stars = pd.read_csv("data/gezari_clean.csv")
        for i in range(53):
            star = stars.iloc[i].to_dict()
            fetch.read_info(star)
    elif sys.argv[1] == 'exps':
        stars = pd.read_csv("data/gezari_clean.csv")
        for i in range(53):
            star = stars.iloc[i].to_dict()
            fetch.read_exposures(star)
    elif sys.argv[1] == 'info_backward':
        stars = pd.read_csv("data/gezari_clean.csv")
        for i in reversed(range(53)):
            star = stars.iloc[i].to_dict()
            fetch.read_info(star)
    elif sys.argv[1] == 'exps_backward':
        stars = pd.read_csv("data/gezari_clean.csv")
        for i in reversed(range(53)):
            star = stars.iloc[i].to_dict()
            fetch.read_exposures(star)
    elif sys.argv[1] == 'fix_info':
        stars = pd.read_csv("data/gezari_clean.csv")
        while True:
            for i in range(53):
                star = stars.iloc[i].to_dict()
                infoFile = 'data/stars/' + star['ID'] + '/info.json'
                if os.path.exists(infoFile):
                    info = fetch.read_info(star)
                    if 'aperture' not in info:
                        print('Fixing info for ' + star['ID'])
                        info['aperture'] = {
                            'rad': 0.0045,
                            'ann': [0.005,0.006]
                        }
                        fetch.write_info(star, info)
            print('Sleeping')
            time.sleep(30)
