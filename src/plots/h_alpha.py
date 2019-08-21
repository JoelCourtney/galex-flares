import query.spectra
import query.sources
import matplotlib.pyplot as plt
import common
import math


# http://www.pas.rochester.edu/~emamajek/EEM_dwarf_UBVIJHK_colors_Teff.txt
MS_color = [-0.037, 0.377, 0.82, 0.98, 1.84, 2.09, 2.25, 2.49, 3.13, 3.95, 4.8]
MS_label = ['A0', 'F0', 'G2', 'K0', 'M0', 'M1', 'M2', 'M3', 'M4.5', 'M6', 'M8']


def create_plot():
    sources = query.sources.get_all_sources()
    powers = []
    colors = []
    for source in sources:
        h_alpha = query.spectra.get_h_alpha(source['SourceID'])
        color = source['Color']
        if source['Distance'] is not None and not math.isnan(h_alpha) and color is not None:
            powers.append(common.flux_to_power(h_alpha, source['Distance']))
            colors.append(color)
    plt.rc('font', family='serif', size=14)
    fig = plt.figure(figsize=(5, 4))
    plt.scatter(colors, powers, color='#EE6677', alpha=0.9)
    plt.xlabel('Gaia $G_{bp} - G_{rp}$')
    plt.ylabel("H-$\\alpha$ Emission (W/ang)")
    # ymin = 0
    # ymax = 5e22
    # plt.ylim([ymin, ymax])
    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    for i in range(4, len(MS_color)-2):
        x = MS_color[i]
        # plt.plot([x, x], [ymin, ymax], color="blue", alpha=0.3, linestyle='dashed')
        plt.text(x, ymin + (ymax-ymin)*0.8, MS_label[i], horizontalalignment='center')
    plt.xlim([xmin, xmax])
    plt.show()


if __name__ == '__main__':
    create_plot()

