import numpy as np
m = 1000
z = np.random.randn(m)
mu = 0.00
sigma = 0.03
theta = 4 * np.random.rand(m) - 1

r = theta * (mu + sigma * z)

x = np.cumprod(1 + r)

figure(1)
clf()
from pylab import *
ion()
# plot(z, alpha=0.5)
# plot(theta, alpha=0.5)
plot(z, alpha=0.5)
plot(x, alpha=1)
plot(range(m), [0] * m)
show()
grid()
