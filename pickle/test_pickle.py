"""
Shows how to do custom serialize via pickle (I think).

Not much effect for this case because it's dumb.
"""
import io
import pdb
import pickle
import time

import numpy as np


def numpy_to_npz_blob(*x):
    buf = io.BytesIO()
    np.savez(buf, *x)
    return buf.getvalue()


def npz_blob_to_numpy(blob):
    f = np.load(io.BytesIO(blob))
    return list(f.values())


class SomethingWithState:
    def __init__(self, m=10000, n=10, k=10, seed=0):
        np.random.seed(seed)
        self.state = [np.random.randn(m, n + i) for i in range(k)]
        self.non_serialized_state = dict(m=m, n=n, k=k, seed=seed)  # should not be present in the unpickled version

    def __repr__(self):
        return self.__class__.__name__ + '\n' + '\n'.join([x.__repr__() for x in self.state])


class SomethingWithStatePickler(SomethingWithState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __getstate__(self, *args, **kwargs):
        return numpy_to_npz_blob(*self.state)

    def __setstate__(self, blob):
        d = npz_blob_to_numpy(blob)
        # dodgy re-assemble but you go get the point, best call a constructor or something
        self.state = d


A = SomethingWithState()
B = SomethingWithStatePickler()

t = time.time()
pA = pickle.dumps(A)
print(time.time() - t)
t = time.time()
pB = pickle.dumps(B)
print(time.time() - t)
print(len(pA), len(pB))

A_ = pickle.loads(pA)
B_ = pickle.loads(pB)

print(B.non_serialized_state)
# print(B_.non_serialized_state)