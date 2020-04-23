import pandas as pd
import numpy.random as nr
import numpy as np

class PandasPiecewiseLinear():
    # dodgy, thing to do piecewise opt
    # this is not useful really, you would need to create some n-d simplex thing ... probably a package that does this
    def __init__(self, x, y):
        """ no extrap """
        self.data = pd.Series(y, index=x)
        assert np.diff(self.data.index.values).min() > 0
    def _reindexed_data(self, x):
        return self.data.reindex(x).interpolate(method='linear')
    def __mul__(self, other):
        data = self.data * other
        return PandasPiecewiseLinear(data.index.values, data.values)
    def __add__(self, other):
        a = self.data.index.values
        b = other.data.index.values
        assert a.min() == b.min()
        assert a.max() == b.max()
        x = np.unique(np.hstack([a, b]))
        x.sort()
        out = self._reindexed_data(x) + other._reindexed_data(x)
        return PandasPiecewiseLinear(out.index.values, out.values)
    def __call__(self, x):
        return si.interp1d(self.data.index.values, self.data.values)(x)
    def __sub__(self, other):
        return self.__add__(other * -1)
    def __repr__(self):
        print('PandasPiecewiseLinear')
        return self.data.__repr__()
    def argmax(self):
        return self.data.idxmax()

# test
# n = 5
# xa = sorted([0] + nr.rand(n).tolist() + [1])
# xb = sorted([0] + nr.rand(n).tolist() + [1])
# a = PandasPiecewiseLinear(xa, list(nr.randn(n + 2)))
# b = PandasPiecewiseLinear(xb, list(nr.randn(n + 2)))
# c = a + b
# c = a - b
# print(c)

import do
F = PandasPiecewiseLinear(do.F.x, do.F.y)
F_ni = PandasPiecewiseLinear(do.F_ni.x, do.F_ni.y)
G = PandasPiecewiseLinear(do.G.x, do.G.y)

F_ttl = F + F_ni

x0 = PandasPiecewiseLinear([0, do._max_x], [1, 1])
x1 = PandasPiecewiseLinear([0, do._max_x], [0, do._max_x])
