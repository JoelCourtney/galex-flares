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

def plot_window(name, window):
    bright = Bright.get(Sources.get(name),window,10)
    print(bright['t0'][0])
    print(bright['t1'][len(bright['t1'])-1])
    bright.plot(x='t0', y='flux')
    plt.title('Flux for ' + name)
    plt.xlabel('Time (GALEX seconds)')
    plt.ylabel('Flux (erg/s/cm^2/A)')
    plt.show()

if __name__ == '__main__':
    plot_window('COSMOS_MOS22-11',0)
