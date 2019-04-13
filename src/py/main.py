#! /usr/bin/env python3

import gPhoton
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import sys
import time
import sources as Sources
import exposures as Exposures
import info as Info
import manual as Man
import bright as Bright

def plotFlare(source, cropped):
    pass
    # flare = 0
    # if cropped:
    #     flare = fetch.read_flare(source)
    # else:
    #     flare = fetch.read_window(source)
    # flare.plot(x="t0",y="flux_mcatbgsub")
    # plt.show()

def main():
    bright = Bright.get(Sources.get('GROTH_MOS05-15'),4)
    print(bright['t0'][0])
    print(bright['t1'][len(bright['t1'])-1])
    bright.plot(x='t0', y='flux')
    plt.title('Flux for GROTH_MOS05-15')
    plt.xlabel('Time (GALEX seconds)')
    plt.ylabel('Flux (erg/s/cm^2/A)')
    plt.show()

if __name__ == '__main__':
    main()
