import json
import numpy as np
import pandas
# _json = '{"2020":{"3":0.16,"5":0.29,"8":1.16},"2021":{"3":0.3,"5":0.66,"8":1.72}}'
_json = '{"2020":{"3":0.11,"5":0.29,"8":0.94},"2021":{"3":0.31,"5":0.60,"8":1.49}}'
d = json.loads(_json)
d = {int(k): {int(kk): vv for kk, vv in v.items()} for k, v in d.items()}

x = np.linspace(1, 8, 100)
from pylab import *
ion()

figure(1)
clf()
for year in d:
    for K in d[year]:
        y = np.maximum(0, K - x)
        subplot(211)
        r = y / d[year][K]
        plot(x, y, label=(year, K))
        subplot(212)
        plot(x, r, label=(year, K))
subplot(211)
legend()
subplot(212)
legend()
show()
