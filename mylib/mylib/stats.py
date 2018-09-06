import scipy.stats as ss
import numpy as np
import scipy.optimize as so

def pareto_from_mean_median(mu, median):
    """
    scipy form has loc and scale.
    (mu - loc) / scale = b / (b - 1)
    (m - loc) / scale = 2 ** (1 / b)

    This problem is abiguous so just force some assumptions.

    b / (b - 1) * 2 ** (-1 / b) = (mu - loc) / (med - loc) ... just choose loc=0, scale=1 for now
    """
    r = mu / median
    def _f(b):
        return (b / (b - 1)) / (2 ** (1 / b)) - r
    b = so.bisect(_f, 1.01, 100)
    loc = 0
    scale = (mu - loc) * (b - 1) / b
    return b, loc, scale
