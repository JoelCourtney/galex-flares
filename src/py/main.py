import gPhoton
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

def main():
    gPhoton.gAperture(band='NUV', skypos=[176.91975, 0.25561], stepsz=10.,
        csvfile='../../data/gj_3685a_lc.csv', radius=0.012,
        annulus=[0.013,0.016],
        trange=[766525335.,766528573.])
    data = pd.read_csv("../../data/gj_3685a_lc.csv")
    data.plot(x="t_mean",y="flux_bgsub")
    plt.show()

if __name__ == '__main__':
    main()
