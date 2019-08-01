import query.sources
import matplotlib.pyplot as plt
import numpy as np
import math


def create_plot():
    sources = query.sources.get_all_sources()
    colors = [source['Color'] for source in sources]
    devs = [(source['FluxSD'] if source['FluxSD'] is not None else float('nan')) * 4 * math.pi *
            ((source['Distance'] if source['Distance'] is not None else float('nan')) * 3.086e18) ** 2
            for source in sources]
    for i in reversed(range(len(colors))):
        if colors[i] is None or devs[i] is None or math.isnan(devs[i]):
            colors.pop(i)
            devs.pop(i)
    plt.rc('font', family='serif', size=14)
    fig = plt.figure(figsize=(5, 4))
    plt.scatter(colors, devs, color='#EE6677', alpha=0.9)
    plt.xlabel('Gaia $G_{bp} - G_{rp}$')
    plt.ylabel('Power StdDev (W/Hz)')
    plt.ylim([0, 5E28])
    plt.show()


if __name__ == '__main__':
    create_plot()
