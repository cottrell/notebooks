"""
plot cumulative taxation rates in uk and canada with some conversion factor

looks wrong
"""
import json
import numpy as np
import pandas as pd
import scipy.interpolate as si

json_data = json.load(open('./taxinfo.json'))
d = dict()
for x in json_data:
    d[(x['country'], x['year'])] = x

a = d[('uk', 2016)]
dfuk = pd.DataFrame(a['data'], columns=a['columns'])
a = d[('canada', 2016)]
dfcan = pd.DataFrame(a['data'], columns=a['columns'])
a = a['province/state']['ontario']
dfont = pd.DataFrame(a['data'], columns=a['columns'])

def get_interp(df):
    x = df['income bucket (left)'].values
    y = df['marginal rate'].values
    x = np.hstack([x, 1e9])
    y = np.hstack([0., y])
    income = np.cumsum(x)
    tax = np.cumsum(x * y)
    return si.interp1d(income, tax, kind='linear')

fuk = get_interp(dfuk)
fcan = get_interp(dfcan)
font = get_interp(dfont)

gbpcad = 1.67 # fx actual
cost_factor = 1.0 # effective cost of living ratio London/Toronto
conversion = gbpcad / cost_factor
# in CAD
x = np.hstack([dfuk['income bucket (left)'].values * conversion, dfcan['income bucket (left)'].values, dfont['income bucket (left)'].values, 3e5, 5e5])
x = np.unique(x)
x.sort()
x_uk = x / conversion
y_uk = fuk(x_uk)
y_cad = fcan(x)
y_ont = font(x)
eps = 0.0001
# df = pd.DataFrame(x, columns=['effective income (CAD)'])
df = pd.DataFrame(x_uk, columns=['effective income (GBP)'])
df['rate UK'] = y_uk / (x_uk + eps)
df['rate Canada total'] = (y_cad + y_ont) / (x + eps)
df['rate Canada fed'] = (y_cad) / (x + eps)
df['rate Canada Ontario'] = (y_ont) / (x + eps)
df = df.set_index(['effective income (GBP)'])

from pylab import *
ion()
figure(1)
clf()
ax = subplot(111)
df.plot(ax=ax, style='o-', logx=False)

df['effective income (GBP)'] = x_uk

figure(2)
clf()
ratio = (df['rate UK'] / df['rate Canada total'])
ax = subplot(111)
ratio.plot(ax=ax, style='o-', logx=False)
plot(ratio.index.values, np.ones(ratio.shape), 'k')
title('UK tax rate to Canada tax rate')
xlabel('income (effective in CAD)')
