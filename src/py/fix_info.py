#! /usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import sources as Sources
import info as Info
import sys
import time
import bright as Bright

def main():
    sources = Sources.all()
    for i in range(53):
        source = sources.iloc[i].to_dict()
        infoFile = 'data/sources/' + source['ID'] + '/info.json'
        if os.path.exists(infoFile):
            info = Info.get(source)
            info['bright_contents'] = ['quiesent']*5
            Info.write(source, info)

def reset_locks():
    sources = Sources.all()
    for i in range(53):
        source = sources.iloc[i].to_dict()
        info = Info.get(source)
        info['locks'] = []
        Info.write(source, info)

def reset_contents():
    sources = Sources.all()
    for i in range(53):
        source = sources.iloc[i].to_dict()
        info = Info.get(source)
        info['bright_contents'] = ['quiesent']*5
        Info.write(source, info)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'reset_locks':
            reset_locks()
        if sys.argv[1] == 'reset_contents':
            reset_contents()
    else:
        main()
