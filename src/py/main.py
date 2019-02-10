import gPhoton

def main():
    gPhoton.gAperture(band='NUV', skypos=[176.91975, 0.25561], stepsz=1.,
        csvfile='../../data/gj_3685a_lc.csv', radius=0.012,
        annulus=[0.013,0.016],
        trange=[766525335,766526573],
        verbose=2)
        #trange=[766525335.,766526573.])

if __name__ == '__main__':
    main()
