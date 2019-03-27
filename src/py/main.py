import gPhoton
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import json
import fetch

def plotFlare(star, cropped):
    flareFile = ''
    if cropped:
        flareFile = 'data/stars/' + star['ID'] + '/flare.csv'
        if not os.path.exists(flareFile):
            fetch.flare(star)
    else:
        flareFile = 'data/stars/' + star['ID'] + '/window.csv'
        if not os.path.exists(flareFile):
            fetch.window(star)
    flare = pd.read_csv(flareFile)
    flare.plot(x="t0",y="flux_mcatbgsub")
    plt.show()

def main():
    stars = pd.read_csv("data/gezari_clean.csv")
    star = stars.iloc[1].to_dict()
    plotFlare(star,True)
    # fetch.flare(star)

if __name__ == '__main__':
    main()
