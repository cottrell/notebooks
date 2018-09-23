"""
In [1]: import do
In [2]: reload(do); l = do.doplot(m=2, d=2); globals().update(l)
"""
import numpy.random as nr
import numpy as np
import iisignature as iis
# consider some d dimensional process, we will later represent it as a *completely broken down stupid form* just to see
d = 3 # dimension of the process
m = 3 # truncation of the signature
n_samples = 10
def vanilla_data_step(dt=1, x0=np.zeros(d)):
    d = x0.shape[0]
    dw = nr.randn(d) * np.sqrt(dt) # whatever
    x = x0 + dw
    return x0 + nr.randn(d) * np.sqrt(dt) # whatever

def vanilla_data(n_samples=n_samples, d=d):
    x = np.zeros(d)
    X = np.zeros((n_samples, d))
    X[0,:] = x
    for i in range(n_samples-1):
        dt = 1
        x = vanilla_data_step(dt=dt, x0=x)
        X[i+1,:] = x
    return X

# def mangled_data_gen(n_samples=n_samples, d=d):
#     # partially observed I guess
#     x = np.zeros(d)
#     out = np.empty((n_samples, 3))
#     t = 0
#     for i in range(n_samples):
#         # observe state
#         j = nr.permutation(range(d))[0]
#         out[i, :] = [t, j, x[j]]
#         # update state
#         dt = 1
#         t = t + dt
#         x = vanilla_data_step(dt=dt, x0=x)
#     # observe final state
#     j = nr.permutation(range(d))[0]
#     out[i, :] = [t, j, x[j]]
#     return out

# remember d changes when you mangle
# s = iis.prepare(d, m)
# x = vanilla_data()
# c = iis.sig(x, m)
# cl = iis.logsig(x, s)
# x = mangled_data_gen()

# up to m = 10 is maybe ok with n_samples = 1000

from pylab import *
ion()
def doplot(n_samples=100, m=5, d=3, nplot=None):
    x = vanilla_data(n_samples=n_samples, d=d)
    # do something to make it interesting: if last coord ever hist 1, then zero out the rest
    hitting_event = np.maximum.accumulate(np.abs(x[:,-1])) > 3
    x[hitting_event,:-1] = 3
    # x[:,:-1] = np.where(cumulative_maximum > 1, 0, x[:,:-1])
    # x = x - x.mean(axis=0)
    # x = x / x.std(axis=0)
    # x = np.exp(x)
    # x = x / x.sum(axis=0)
    s = iis.prepare(d, m)
    if nplot is None:
        nplot = n_samples
    ii = n_samples // nplot
    figure(1)
    clf()
    ax = subplot(2,1,1)
    plot(x, alpha=0.5)
    ylabel('path')
    t = list()
    data = list()
    for i in range(ii, n_samples, ii):
        t.append(i)
        temp = iis.logsig(x[:i], s)
        data.append(temp)
    data = np.array(data)
    assert data.shape[1] == iis.logsiglength(d, m), 'not match!'
    t = np.array(t)
    ax = subplot(2,1,2)
    plot(t, (data.T / (t ** 0)).T, alpha=0.5)
    # plot(t, (data[:,-1].T / (t ** 0)).T, alpha=0.5)
    ylabel('logsig')
    xlabel('t')
    show()
    return locals()

