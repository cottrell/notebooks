#!/usr/bin/env python
import functools
import sys
import time

import numpy as np
import scipy.linalg


def run(kind):
    if kind == 'numpy':
        fun = np.linalg.lstsq
    elif kind == 'scipy_gelsd':
        fun = functools.partial(scipy.linalg.lstsq, lapack_driver='gelsd')
    elif kind == 'scipy_gelsy':
        fun = functools.partial(scipy.linalg.lstsq, lapack_driver='gelsy')
    else:
        raise Exception(f'no idea {kind}')

    seed = 0
    m = 25498
    n = 2369

    np.random.seed(seed)
    A = 2 * np.random.rand(m, n) - 1
    b = 2 * np.random.rand(m) - 1

    seconds = 1
    print(f'sleeping for {seconds} seconds to see any spikes')
    time.sleep(seconds)
    print(f'solving lstsq with A.shape={A.shape} b.shape={b.shape}')
    u = np.linalg.lstsq(A, b, rcond=None)[0]

    seconds = 2
    print('deleting A b but not u and then sleeping for {seconds} seconds')
    del A
    del b
    time.sleep(seconds)


if __name__ == '__main__':
    kind = sys.argv[1]
    print(kind)
    run(kind)
