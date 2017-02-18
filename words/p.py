#!/usr/bin/env python
import pandas as pd

def parse():
    df = pd.read_csv('data/stacked.txt', header=None)
    df = df.dropna(how='any')
    allwords = sorted(list(set(df[0].unique().tolist() + df[1].unique().tolist())))
    df = df.sort_values(by=0)
    for k in df:
        df[k] = pd.Categorical(df[k].values, allwords)
    return df

if __name__ == '__main__':
    fout = open('data/stacked.txt', 'w')
    for line in open('data/mthesaur.txt'):
        row = line.strip().split(',')
        if len(row) <= 1:
            continue
        base = row[0].strip()
        for x in row[1:]:
            print('{},{}'.format(base, x.strip()), file=fout)
