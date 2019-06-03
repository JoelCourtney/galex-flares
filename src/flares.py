#! /usr/bin/env python3

import matplotlib.pyplot as plt
import data


def delimit_flare(sourceID):
    flare = data.get_lightcurve(sourceID)
    exps = data.get_exposures(sourceID)
    for r in range(len(exps)):
        times = []


        def onclick(event):
            global ix, iy
            ix, iy = event.xdata, event.ydata
            print('x = %d, y = %d' % (
                ix, iy))
            times.append(round(ix))
            if ix is None:
                print("No flare")
                fig.canvas.mpl_disconnect(cid)
                plt.close(fig)
                times.clear()
            elif iy is None:
                print("Bad flare")
                fig.canvas.mpl_disconnect(cid)
                plt.close(fig)
            elif len(times) == 2:
                print('Please delimit quiesent period')
            elif len(times) == 4:
                fig.canvas.mpl_disconnect(cid)
                plt.close(fig)

        t0 = exps.iloc[r]['t0']
        t1 = exps.iloc[r]['t1']
        exp = flare.loc[(flare['t0'] >= t0) & (flare['t1'] <= t1)]
        fig = exp.plot(x='t0', y='flux').get_figure()
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        print(sourceID)
        plt.show()


def delimit_all_flares():
    print("Delimit flares if possible.")
    print("Bad x = no flare")
    print("Bad y = bad flare")
    for i in range(1, 54):
        source = data.get_source(i)
        delimit_flare(source['SourceID'])


if __name__ == '__main__':
    delimit_all_flares()
