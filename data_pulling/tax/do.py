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

_max_x = 3e5

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

def get_pension_limit(v):
    x, y = zip(*v)
    x = np.hstack([x, _max_x])
    y = np.hstack([y, y[-1]])
    f = si.interp1d(x, y, fill_value=(y[0], y[-1]), kind='linear', bounds_error=False)
    return f

check, m_F, F = get_tax_interp(v_tax)
check_ni, m_F_ni, F_ni = get_tax_interp(v_tax_ni)
G = get_pension_limit(v_pension)

assert F(200000) == 75600


def doplot():
    x = linspace(1, _max_x, 10000)
    figure(1)
    ion()
    clf()
    subplot(311)
    grid()
    plot(x, m_F(x), '-', label='tax')
    plot(x, m_F_ni(x), '-', label='ni')
    legend()
    ylabel('marginal rate')
    subplot(312)
    grid()
    plot(x, F(x), '-', label='tax')
    plot(x, F_ni(x), '-', label='ni')
    ylabel('tax and pension limit')

    plot(x, G(x), '-', label='pension limit')

    subplot(313)
    grid()
    # plot(x, x, 'k-', label='gross')
    total_no_contribution = F(x) + F_ni(x)
    total_max_contribution = F(x - G(x)) + F_ni(x - G(x))
    plot(x, total_no_contribution, label='total no contrib')
    plot(x, total_max_contribution, label='total max contrib')
    plot(x, total_no_contribution - total_max_contribution, label='tax delta')
    ylabel('income and tax')
    legend()
    show()

    max_scenario_effective_rate = total_max_contribution / x
    zero_scenario_effective_rate = total_no_contribution / x
    figure(2)
    clf()
    grid()
    plot(x, max_scenario_effective_rate, '--', label='max scenario')
    plot(x, zero_scenario_effective_rate, '--', label='zero scenario')
    legend()
    ylabel('effective tax rate')
    xlabel('income')
    title('one year only')

def get_tax_info(gross, pension_contribution):
    g = G(gross)
    if pension_contribution == 'max':
        pension_contribution = g
    assert pension_contribution <= g, 'pension contrib greater than max {} > {}'.format(pension_contribution, g)
    taxable = gross - pension_contribution
    tax = F(taxable)
    ni = F_ni(taxable)
    net = gross - tax - ni
    effective_tax_rate = 1 - net / gross
    return dict(gross=gross, net=net, pension_contribution=pension_contribution, pension_room=g, ni=ni, tax=tax, effective_tax_rate=effective_tax_rate)
