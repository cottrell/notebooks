from pylab import *
import numpy as np

def nfft_example():
    # git@github.com:jakevdp/nfft.git
    m = 1000
    x = np.random.rand(m) * 2 - 1
    x.sort()
    y = np.cos(2 * np.pi * x) # + np.sin(10 * np.pi * x)
    import nfft
    M = 16

    # y_hat = nfft.ndft_adjoint(x, y, M)
    # y_hat /= m
    # y_ = nfft.ndft(x, y_hat)

    y_hat = nfft.nfft_adjoint(x, y, M)
    y_hat /= m
    y_ = nfft.nfft(x, y_hat)
    print(y.shape, y_hat.shape, y_.shape)
    doplot(x, y, y_hat, y_)

def doplot(x, y, y_hat, y_, fig=1):
    fig = figure(fig)
    fig.clf()
    ax_ = fig.subplots(3, 1)
    ion()

    ax = ax_[0]
    ax.plot(x, y, 'o', label='orig')
    ax.legend()

    ax = ax_[1]
    M = len(y_hat)
    k = np.arange(-M // 2, M // 2)
    ax.plot(k, np.real(y_hat), 'o', label='y_hat')
    ax.legend()

    ax = ax_[2]
    ax.plot(x, np.real(y_), 'o', label='round_trip')
    ax.legend()
    fig.show()

def pynufft_example():
    m = 1000
    x = np.random.randn(m)
    x.sort()
    y = np.sin(2 * np.pi * x) # + np.sin(10 * np.pi * x)
    from pynufft import NUFFT
    nu = NUFFT()
    M = 256
    Nd = (M,)
    Kd = (2 * M,)  # oversampling is probably some implicit probablistic smoothing prior
    Jd = (6,)  # interpolator size
    nu.plan(x[:, None], Nd, Kd, Jd)
    y_hat = nu.adjoint(y)
    y_ = nu.forward(y_hat)


