import query.sources
import matplotlib.pyplot as plt
import numpy as np


def create_plot():
    sources = query.sources.get_all_sources()
    colors = [source['Color'] for source in sources]
    devs = [source['FluxSD'] for source in sources]
    for i in reversed(range(len(colors))):
        if colors[i] is None or devs[i] is None or devs[i] > 1E-12:
            colors.pop(i)
            devs.pop(i)
    plt.rc('font', family='serif', size=14)
    fig = plt.figure(figsize=(10, 8))
    plt.scatter(colors, devs, color='#EE6677', alpha=0.9)
    plt.xlabel('Bp-Rp')
    plt.ylabel('Flux StdDev')
    plt.ylim([np.min(devs), np.max(devs)])
    plt.show()


if __name__ == '__main__':
    create_plot()
