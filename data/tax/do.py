from pylab import *
import pandas as pd
import os
import scipy.interpolate as si
import json
import numpy as np
json_data = json.load(open('./taxinfo.json'))
d = dict()
for x in json_data:
    d[(x['country'], x['year'])] = x

df = d[('uk', '2018-2019')]
v_tax = df['income_tax']['data']
v_tax_ni = df['data_employee_ni']['data'] # not sure
v_pension = df['data_pension_limit']['data']

_max_x = 5e5

def get_tax_interp(v):
    """ marginals and boundaries """
    x, y = zip(*v)
    xx = np.hstack([x, _max_x])
    tax = (xx[1:] - xx[:-1]) * y
    check = pd.DataFrame(list(zip(xx[:-1], xx[1:], y, tax)), columns=['left', 'right', 'rate', 'tax'])
    check['tax_cumulative'] = check.tax.cumsum()
    # marginal, extrapolate is just flat fill for zero
    m = si.interp1d(check.left.values, check.rate.values, kind='zero', fill_value='extrapolate')
    # extrapolate, linear is correct for cumsum
    # cumulative, using rhs ... this is confusing
    t = si.interp1d(np.hstack([0, check.right.values]),
        np.hstack([0, check.tax_cumulative.values]), kind='linear', fill_value='extrapolate')
    return check, m, t

check, m_F, F = get_tax_interp(v_tax)
check_ni, m_F_ni, F_ni = get_tax_interp(v_tax_ni)

assert F(200000) == 75600

x = linspace(0, 300000)
figure(1)
ion()
clf()
subplot(211)
grid()
plot(x, m_F(x), '.-')
subplot(212)
grid()
plot(x, F(x), '.-')

def get_pension_limit(v):
    x, y = zip(*v)
    f = si.interp1d(x, y, fill_value=(y[0], y[-1]), kind='linear', bounds_error=False)
    return f

G = get_pension_limit(v_pension)
plot(x, G(x), '.-')

show()
