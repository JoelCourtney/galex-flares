#! /usr/bin/env python3

import data as Data
import pandas as pd

def do_it():
    sources = pd.read_csv("../gezari_clean.csv")
    for i in range(53):
        row = sources.iloc[i].to_dict()
        Data.insert_source(row['ID'],row['RAdeg'],row['DEdeg'])

if __name__ == '__main__':
    do_it()
