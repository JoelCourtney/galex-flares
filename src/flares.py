#! /usr/bin/env python3

import matplotlib.pyplot as plt
import data
import numpy as np
import math


def delimit_flare(sourceID):
    data.delete_flares(sourceID)
    flare = data.get_lightcurve(sourceID)
    if flare.empty:
        return False
    exps = data.get_exposures(sourceID)
    for r in range(len(exps)):
        times = []

        def onclick(event):
            global ix, iy
            ix, iy = event.xdata, event.ydata
            print('x = %d, y = %d' % (
                ix, iy))
            times.append(round(ix))
            if len(times) == 2:
                print('Please delimit quiesent period')
            elif len(times) == 4:
                fig.canvas.mpl_disconnect(cid)
                plt.close(fig)

        t0 = exps.iloc[r]['t0']
        t1 = exps.iloc[r]['t1']
        exp = flare.loc[(flare['t0'] >= t0) & (flare['t1'] <= t1)]
        if not exp.empty:
            fig = exp.plot(x='t0', y=['flux', 'flux_bgsub']).get_figure()
            cid = fig.canvas.mpl_connect('button_press_event', onclick)
            print(sourceID)
            bottom, top = plt.ylim()
            if bottom < -1.e-14:
                plt.ylim(bottom=-1.e-14)
            if top > 1.e-14:
                plt.ylim(top=1.e-14)
            plt.show()
            if len(times) == 1:
                data.insert_flare(sourceID, False, t0, t1)
            elif len(times) == 4:
                data.insert_flare(sourceID, True, times[0], times[1], times[2], times[3])
        else:
            print("No data in exposure")
    return True


def delimit_all_flares():
    print("Delimit flares if possible.")
    print("Close window = no flare")
    print("One click = bad flare")
    for i in range(1, 54):
        source = data.get_source(i)
        if data.create_lock(source['SourceID'], 'flares'):
            if delimit_flare(source['SourceID']):
                data.change_lock(source['SourceID'], 'flares', 'complete')
            else:
                data.release_lock(source['SourceID'], 'flares')


def calculate_energy(flare):
    flare_lc = data.get_lightcurve_range(flare['SourceID'], flare['FlareStart'], flare['FlareEnd'])
    # flare_lc.plot(x='t0', y='flux')
    # plt.show()
    quiesent_lc = data.get_lightcurve_range(flare['SourceID'], flare['QuiesentStart'], flare['QuiesentEnd'])
    quiesent_mean = quiesent_lc.mean(axis=0)['flux_bgsub']
    area = np.trapz(flare_lc['flux_mcatbgsub'] - quiesent_mean, x=flare_lc['t0'])
    parallax = data.get_parallax(flare['SourceID'])
    if parallax == None:
        parallax = float('nan')
        print(flare['SourceID'])
    distance = 1000 / parallax
    distance *= 3.086e18
    bandwidth = 1050
    energy = area * 4 * math.pi * (distance ** 2) * bandwidth
    return energy


def calculate_all_energies():
    energies = []
    flares = data.get_good_flares()
    discarded = 0
    for flare in flares:
        energy = calculate_energy(flare)
        if energy and not math.isnan(energy):
            data.set_energy(flare['FlareID'], energy)
            energies.append(calculate_energy(flare))
        else:
            discarded += 1
    print("Discarded: " + str(discarded))
    print(np.median(energies))


def plot_energies():
    energies = [energy['Energy'] for energy in data.get_all_energies()]
    print(energies)
    plt.hist(energies)
    plt.gca().set_xscale('log')
    plt.xlabel('NUV Energy of Flare (ergs)')
    plt.ylabel('# Occurances')
    plt.title('Energy Distribution of Flares')
    plt.show()


def show_flares_for_source(Source):
    flares = data.get_good_flares_for_source(Source)
    for flare in flares:
        print(flare['FlareID'])
        lc = data.get_lightcurve_range(flare['SourceID'], flare['FlareStart']-500, flare['FlareEnd']+500)
        lc.plot(x='t0', y='flux')
        plt.show()


def show_all_good_flares():
    flares = data.get_good_flares()
    for flare in flares:
        print(flare['SourceID'])
        print(flare['FlareID'])
        lc = data.get_lightcurve_range(flare['SourceID'], flare['FlareStart']-500, flare['FlareEnd']+500)
        print(lc)
        if not lc.empty:
            lc.plot(x='t0', y='flux')
            plt.show()


if __name__ == '__main__':
    # calculate_all_energies()
    # plot_energies()
    # flare = data.get_flare(6)
    # show_flares_for_source('COSMOS_MOS25-12')
    # print(calculate_energy(flare))
    # delimit_all_flares()
    show_all_good_flares()
