import numpy.random as nr
import pandas as pd
import numpy as np
import scipy.stats as ss
from pylab import *
ion()

def pareto_junk(m=10000, n=1, b=0.5):
    s = ss.pareto(b).rvs(m)
    a = np.empty((m, n))
    for i in range(n):
        a[:,i] = pd.Series(nr.permutation(s)).expanding(min_periods=100).mean().values
    d = pd.DataFrame(a)
    figure(1)
    clf()
    ax = gca()
    # nn = m // 200
    # d.loc[::nn].plot(ax=ax)
    d.plot(ax=ax)
    show()
    globals().update(locals())
