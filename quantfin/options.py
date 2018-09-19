# vanilla call from https://ipythonquant.wordpress.com/2018/05/22/tensorflow-meets-quantitative-finance-pricing-exotic-options-with-monte-carlo-simulations-in-tensorflow/
import scipy.stats as stats
import numpy as np


def vanilla(S_0, strike, time_to_expiry, implied_vol, riskfree_rate, kind='put'):
    S = S_0
    K = strike
    dt = time_to_expiry
    sigma = implied_vol
    r = riskfree_rate
    Phi = stats.norm.cdf
    d_1 = (np.log(S_0 / K) + (r + (sigma**2) / 2) * dt) / (sigma * np.sqrt(dt))
    d_2 = d_1 - sigma * np.sqrt(dt)
    if kind == 'call':
        return S * Phi(d_1) - K * np.exp(-r * dt) * Phi(d_2)
    elif kind == 'put':
        return - S * Phi(-d_1) + K * np.exp(-r * dt) * Phi(-d_2)
    else:
        raise Exception('dunno kind = {}'.format(kind))


v = vanilla(100., 110., 2., 0.2, 0.03)

def q(S_0=100, strike=110, time_to_expiry=1, implied_vol=.2, riskfree_rate=0.00):
    return vanilla(S_0, strike, time_to_expiry, implied_vol, riskfree_rate)
