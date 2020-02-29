from pylab import *
import pandas as pd
url = open('./co2_per_km2.csv').readline()[1:].strip()
df = pd.read_csv('./co2_per_km2.csv', comment='#')

ion()
fig = figure(1, figsize=(8, 6))
clf()

rot = 0
for i in range(df.shape[0] - 1):
    x = df.iloc[i].values
    plot(x[2], x[1], 'o')
    text(x[2], x[1], x[0], fontsize=6, alpha=0.75, rotation=rot)

i = df.shape[0] - 1
x = df.iloc[i].values
plot(x[2], x[1], 'ro', markersize=10, alpha=0.75)
text(x[2], x[1], x[0], fontsize=6, alpha=0.75, rotation=rot)
world = x[1]
plot(xlim(), [world, world], 'r', alpha=0.25, linewidth=5)

ax = gca()
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_ylabel(df.columns[1])
ax.set_xlabel(df.columns[2])
title(url, fontsize=8)
tight_layout()
