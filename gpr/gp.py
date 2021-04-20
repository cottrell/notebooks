import numpy as np
import scipy.spatial.distance as dist

class GP:
    def __init__(self, kernel=sqexp_kernel, sigma=1.0):
        self.kernel = kernel
        self.sigma = sigma

    def fit(self, X, y):
        self.X = X  # hstack(self.X, X)
        self.y = y  # hstack(self.y, y)
        self.K = self.kernel(self.X, self.X)
        self.Ky = self.K + self.sigma ** 2 * np.eye(self.K.shape[0])

    def predict(self, xtest):
        """ compute mu_star, K_star, sigma_star """
        Ks = self.kernel(self.X, xtest)
        Kss = self.kernel(xtest, xtest)

        # np.solve ?
        Kyinv = np.linalg.inv(self.Ky)
        KKyT = np.dot(Ks.T, Kyinv)

        mu = np.dot(KKyT, self.y)
        Ss = Kss - np.dot(KKyT, Ks)
        return mu, Ss

def sqexp_kernel(x1, x2, ell=.5, sf2=1.0):
    """ x1 and x2 of size (n, d) and (m, d) """
    d = dist.cdist(x1, x2, 'sqeuclidean')
    k = sf2 * np.exp(-0.5 * d / ell)
    return k
