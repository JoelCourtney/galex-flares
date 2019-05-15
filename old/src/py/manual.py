#! /usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import exposures as Exposures
import info as Info
import sources as Sources
import sys
import bright as Bright
import flares as Flares

def delimit(source, n):
    times = []
    def onclick(event):
        global ix, iy
        ix, iy = event.xdata, event.ydata
        print('x = %d, y = %d'%(
            ix, iy))
        times.append(round(ix))
        if len(times) == 2:
            print('Please delimit quiesent period')
        elif len(times) == 4:
            fig.canvas.mpl_disconnect(cid)
            plt.close(fig)

    bright = Bright.get(source, n)
    fig = bright.plot(x="t0",y="flux").get_figure()
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    print('Please delimit flare ' + str(n) + ' for ' + source['ID'])
    plt.show()
    return times

def classify(source, n):
    result = ['quiesent']
    def onclick(event):
        ix = event.xdata
        iy = event.ydata
        if ix == None:
            result[0] = 'bad'
        elif ix > t_mid:
            result[0] = 'flare'
        else:
            result[0] = 'dubious'
        fig.canvas.mpl_disconnect(cid)
        plt.close(fig)

    bright = Bright.get(source, n)
    t_left = bright['t0'].iloc[0]
    t_right = bright['t1'].iloc[-1]
    t_mid = (t_left+t_right)/2
    fig = bright.plot(x="t0",y="flux").get_figure()
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    print('Please classify bright exposure ' + str(n) + ' for ' + source['ID'])
    plt.show()
    print(result[0])
    return result[0]

def main():
    if sys.argv[1] == 'delimit':
        flares = Flares.read_info()
        for i in range(len(flares)):
            source = Sources.get(flares[i]['source'])
            n = flares[i]['bright_window']
            times = delimit(source, n)
            Flares.write_times(i, [times[0],times[1]],[times[2],times[3]])
    if sys.argv[1] == 'classify':
        for i in range(53):
            source = Sources.get(row=i)
            info = Info.get(source)
            for f in range(5):
                if info['bright_contents'][f] in ['bad','quiesent','flare']:
                    result = classify(source, f)
                    info['bright_contents'][f] = result
            Info.write(source, info)



if __name__ == '__main__':
    main()
