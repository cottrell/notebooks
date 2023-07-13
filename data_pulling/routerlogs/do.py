#!/usr/bin/env python
import os
import datetime
import pandas as pd
df = pd.read_csv('data/timeseries.csv')
# df['date'] = df.date.apply(lambda x: datetime.datetime.strptime(x, '%A, %B %d,%Y %H:%M:%S'))
df['date'] = df.date.apply(lambda x: pd.to_datetime(x))
df['ip'] = df.ip.apply(lambda x: x.split(':')[0])
df['dt'] = df.date.dt.round('1min')

who = list()
for k in df['ip'].unique():
    filename = os.path.join('data/whois', k)
    text = open(filename).read().split('\n')
    d = (x.strip() for x in text)
    d = (x for x in d if x and not x.startswith('%') and not x.startswith('#'))
    d = ([xx.strip() for xx in x.split(':', 1)] for x in d)
    d = (x for x in d if len(x) == 2)
    d = list(d)
    d = dict(d)
    d['ip'] = k
    who.append(d)
d_ = pd.DataFrame(who)
n = d_.shape[0]
s = d_.count() / n
d_ = d_.loc[:, s[s > 0.8].index]   # only high avail stuff
cols = ['OrgName', 'Country', 'City', 'Organization', 'ip']
d_ = d_[cols]

d = df.groupby(['dt', 'ip']).size().reset_index()

d = d.set_index('ip')
d_ = d_.set_index('ip')
d = d.join(d_)
d = d.reset_index()
cols = ['dt'] + cols
d = d[cols]
d = d.sort_values(cols)

print(d.shape)
print(d.to_string())
# d.unstack('ip').fillna(0).plot()
# from pylab import *
# ion()
# os.makedirs('data/img/', exist_ok=True)
# savefig('data/img/a.png')
