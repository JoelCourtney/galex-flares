import gPhoton
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import sys
import time
import sources as Sources
import exposures as Exposures
import info as Info
import manual as Man
import bright as Bright

def main():
    if len(sys.argv) == 2:
        for i in range(53):
            source = Sources.get(row=i)
            contents = Info.get(source)['bright_contents']
            for n,c in enumerate(contents):
                if c == sys.argv[1]:
                    print(source['ID'])
                    flare = Bright.get(source, n)
                    flare.plot(x='t0', y='flux')
                    plt.show()


if __name__ == '__main__':
    main()
