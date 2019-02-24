from pylab import *
import pandas as pd
import numpy as np
import scipy.stats
normdist = scipy.stats.norm()
m = 1000
epsilon = 0.5
rho = 1
mu = 0.00
sigma = 0.03

def get_samples():
    X = list()
    TH = list()
    Z = list()
    for i in range(100):
        zz = np.random.randn(m)
        z = np.sqrt(1 - epsilon ** 2) * np.random.randn(m) + rho * epsilon * zz
        u = normdist.cdf(np.sqrt(1 - epsilon ** 2) * np.random.randn(m) + epsilon * zz)
        theta = 1 * (2 * u - 1)
        r = theta * (mu + sigma * z)
        x = np.cumprod(1 + r)
        X.append(x)
        TH.append(theta)
        Z.append(z)
    X = np.vstack(X).T
    TH = np.vstack(TH).T
    Z = np.vstack(Z).T
    return X, TH, Z

x, theta, z = get_samples()

c = pd.DataFrame(theta * z)
print('accuracy')
print((c > 0).stack().sum() / np.prod(c.shape))

ion()
figure(1)
clf()
plot(x, alpha=0.05)
plot(range(m), [1] * m)
show()
grid()
df = pd.DataFrame(x)
ax = gca()
df.mean(axis=1).plot(ax=ax)

# figure(2)
# clf()
# plot(theta, r, '.')
