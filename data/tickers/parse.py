#!/usr/bin/env python
# this is a mess
import json
import os
import pandas as pd
import glob
files = glob.glob('excel_to_csv/*/*.csv')
files = [f for f in files if 'About' not in f]
dfs = list()
for f in files:
    df = pd.read_csv(f, skiprows=3)
    df['Product'] = os.path.basename(f).split('.')[0]
    dfs.append(df)
df = pd.concat(dfs, sort=False)
cols = ['Product', 'Ticker', 'Name', 'Exchange', 'Category Name', 'Country']
df = df[cols]
df.columns = [x.lower() for x in df.columns]
df['source'] = 'investexcel.net/all-yahoo-finance-stock-tickers/'

d = json.load(open('../../kaggle/price-volume-data-for-all-us-stocks-etfs/meta.json'))
a = pd.DataFrame(d['etfs'], columns=['ticker'])
a['product'] = 'etf'
b = pd.DataFrame(d['stocks'], columns=['ticker'])
b['product'] = 'stock'
dd = pd.concat([a, b], axis=0)
dd['source'] = 'kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs'

a = [x for x in d['stocks'] + d['etfs']]
b = [x.split('.')[0] for x in df[df['product'].isin(['etf', 'stock'])].ticker.tolist()]

df = pd.concat([df, dd], axis=0)
df = df.sort_values(['product', 'ticker'])

df.to_csv('yahoo_tickers.csv', index=False)
