#! /usr/bin/env python3

import matplotlib.pyplot as plt
import query.flares
import query.lightcurves
import query.misc
import query.sources
import numpy as np
import math


def delimit_flare(sourceID):
    query.flares.delete_flares(sourceID)
    flare = query.lightcurves.get_lightcurve(sourceID)
    if flare.empty:
        return False
    exps = query.lightcurves.get_exposures(sourceID)
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
                query.flares.insert_flare(sourceID, False, t0, t1)
            elif len(times) == 4:
                query.flares.insert_flare(sourceID, True, times[0], times[1], times[2], times[3])
        else:
            print("No data in exposure")
    return True


def delimit_all_flares():
    print("Delimit flares if possible.")
    print("Close window = no flare")
    print("One click = bad flare")
    for i in range(1, 54):
        source = query.sources.get_source(i)
        if query.locks.create_lock(source['SourceID'], 'flares'):
            if delimit_flare(source['SourceID']):
                query.locks.change_lock(source['SourceID'], 'flares', 'complete')
            else:
                query.locks.release_lock(source['SourceID'], 'flares')


def calculate_energy(flare):
    flare_lc = query.lightcurves.get_lightcurve_range(flare['SourceID'], flare['FlareStart'], flare['FlareEnd'])
    # flare_lc.plot(x='t0', y='flux')
    # plt.show()
    quiesent_lc = query.lightcurves.get_lightcurve_range(flare['SourceID'], flare['QuiesentStart'], flare['QuiesentEnd'])
    quiesent_mean = quiesent_lc.mean(axis=0)['flux_bgsub']
    area = np.trapz(flare_lc['flux_mcatbgsub'] - quiesent_mean, x=flare_lc['t0'])
    distance = query.sources.get_distance(flare['SourceID']) * 3.086e18
    bandwidth = 1050
    energy = area * 4 * math.pi * (distance ** 2) * bandwidth
    return energy


def calculate_all_energies():
    energies = []
    flares = query.flares.get_good_flares()
    discarded = 0
    for flare in flares:
        energy = calculate_energy(flare)
        if energy and not math.isnan(energy):
            query.flares.set_energy(flare['FlareID'], energy)
            energies.append(energy)
        else:
            discarded += 1
    print("Discarded: " + str(discarded))
    print(np.median(energies))


def show_flares_for_source(Source):
    flares = query.flares.get_good_flares_for_source(Source)
    for flare in flares:
        print(flare['FlareID'])
        lc = query.lightcurves.get_lightcurve_range(flare['SourceID'], flare['FlareStart']-500, flare['FlareEnd']+500)
        lc.plot(x='t0', y='flux')
        plt.show()


def show_all_good_flares():
    flares = query.flares.get_good_flares()
    for flare in flares:
        print(flare['SourceID'])
        print(flare['FlareID'])
        lc = query.lightcurves.get_lightcurve_range(flare['SourceID'], flare['FlareStart']-500, flare['FlareEnd']+500)
        print(lc)
        if not lc.empty:
            lc.plot(x='t0', y='flux')
            plt.show()


def auto_detect(lc, mean, thresh, exps):
    count = 0
    for i in range(len(exps)):
        exp = exps.iloc[i]
        partial_lc = lc.loc[(lc['t0'] >= exp['t0']) & (lc['t1'] <= exp['t1'])]
        flags = partial_lc['flux'] > thresh
        if flags.any():
            true_flags = flags[flags==True]
            first_flag, last_flag = true_flags.first_valid_index(), true_flags.last_valid_index()
            while first_flag > partial_lc.first_valid_index():
                first_flag -= 1
                if partial_lc['flux'][first_flag] < mean:
                    break
            while last_flag < partial_lc.last_valid_index():
                last_flag += 1
                if partial_lc['flux'][last_flag] < mean:
                    break
            partial_lc.plot(x='t0', y=['flux', 'flux_bgsub'])
            plt.plot([exp['t0'], exp['t1']], [thresh, thresh], color='green', alpha=0.5)
            plt.plot([exp['t0'], exp['t1']], [mean, mean], color='green', alpha=0.5)
            ymin, ymax = plt.ylim()
            plt.plot([partial_lc['t0'][first_flag], partial_lc['t0'][first_flag]], [ymin, ymax], color='gray', alpha=0.5)
            plt.plot([partial_lc['t1'][last_flag], partial_lc['t1'][last_flag]], [ymin, ymax], color='gray', alpha=0.5)
            plt.show()
            count += 1
    print(count)
    return count


def auto_detect_all():
    ids = []
    lcs = []
    for id in query.sources.get_ids():
        if id['SourceID'] != 'gj_3685a':
            lc = query.lightcurves.get_lightcurve_fluxes(id['SourceID'])
            mean = np.mean(lc[['flux']])['flux']
            lc['flux'] /= mean
            lcs.append(lc)
            ids.append(id['SourceID'])
    sd = 0
    n = 0
    for lc in lcs:
        for f in lc['flux'].tolist():
            try:
                sd += (f-1)**2
            except Exception as e:
                print(f['flux'])
                print(sd)
                print(e)
                return
            n += 1
    sd = math.sqrt(sd/(n-1))
    thresh = 1+5*sd
    count = 0
    for i in range(len(lcs)):
        id = ids[i]
        lc = lcs[i]
        exps = query.misc.get_exposures(id)
        print(id)
        count += auto_detect(lc, 1, thresh, exps)
    print(count)


if __name__ == '__main__':
    auto_detect_all()
    # calculate_all_energies()
