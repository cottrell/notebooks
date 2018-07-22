# used in that flylsh hack
import scipy.sparse
import numpy as np

def mean_shift_nonzero_sparse(data):
    # shift rows
    # probably inplace
    assert scipy.sparse.isspmatrix_csr(data), 'must use csr format'
    # adjust zero elements only ... kind of strange
    m = np.array(data.sum(axis=1)).squeeze()
    nonzero_per_row = np.diff(data.indptr) # https://stackoverflow.com/questions/3797158/counting-non-zero-elements-within-each-row-and-within-each-column-of-a-2d-numpy
    data_mean = m / nonzero_per_row
    data.data -= data_mean[data.indices]
    return data
