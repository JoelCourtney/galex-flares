import query.sources
import matplotlib.pyplot as plt
import numpy as np
import math

MS_color = [-0.037, 0.377, 0.82, 0.98,1.84,2.09,2.25,2.49,3.13,3.95,4.8]  #http://www.pas.rochester.edu/~emamajek/EEM_dwarf_UBVIJHK_colors_Teff.txt
MS_label = ['A0', 'F0', 'G2', 'K0', 'M0', 'M1', 'M2', 'M3', 'M4.5', 'M6', 'M8']


def create_plot():
    sources = query.sources.get_all_sources()
    colors = [
        source['Color']
        for source in sources
        if source['FluxSD'] is not None and source['Distance'] is not None and source['Color'] is not None
    ]
    devs = [
        source['FluxSD'] * 4 * math.pi * (source['Distance'] * 3.086E18)**2 * 1e-7
        for source in sources
        if source['FluxSD'] is not None and source['Distance'] is not None and source['Color'] is not None
    ]
    plt.rc('font', family='serif', size=14)
    fig = plt.figure(figsize=(5, 4))
    plt.scatter(colors, devs, color='#EE6677', alpha=0.9)
    plt.xlabel('Gaia $G_{bp} - G_{rp}$')
    plt.ylabel('Power StdDev (W/nm)')
    ymin = 0
    ymax = 5e21
    plt.ylim([ymin, ymax])
    xmin, xmax = plt.xlim()
    for i in range(3, len(MS_color)-2):
        x = MS_color[i]
        # plt.plot([x, x], [ymin, ymax], color="blue", alpha=0.3, linestyle='dashed')
        plt.text(x, ymin + (ymax-ymin)*0.8, MS_label[i], horizontalalignment='center')
    plt.xlim([xmin, xmax])
    plt.show()


if __name__ == '__main__':
    create_plot()
