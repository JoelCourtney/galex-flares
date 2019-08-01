import query.flares
import matplotlib.pyplot as plt
import numpy as np


def create_plot():
    energies = [energy['Energy'] for energy in query.flares.get_all_energies()]
    print(energies)
    plt.hist(energies, bins=np.logspace(30, 35, 20))
    plt.gca().set_xscale('log')
    plt.xlabel('NUV Energy of Flare (ergs)')
    plt.ylabel('# Occurances')
    plt.title('Energy Distribution of Flares')
    plt.show()


if __name__ == '__main__':
    create_plot()