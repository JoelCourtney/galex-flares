import pandas as pd
import matplotlib.pyplot as plt
import exposures as Exposures
import info as Info
import sources as Sources
import sys
import bright as Flare

def delimit(source, n):
    times = []
    def onclick(event):
        global ix, iy
        ix, iy = event.xdata, event.ydata
        print('x = %d, y = %d'%(
            ix, iy))
        times.append(round(ix))

    flare = Flare.get(source, n)
    fig = flare.plot(x="t0",y="flux_bgsub").get_figure()
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    print('Please delimit flare ' + str(n) + ' for ' + source['ID'])
    plt.show()
    return times

def main():
    if sys.argv[1] == 'delimit':
        for i in range(53):
            source = Sources.get(row=i)
            for f in range(5):
                print(delimit(source, f))


if __name__ == '__main__':
    main()
