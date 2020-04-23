cimport numpy as np

cdef inline inc(int* arr, int i):
    arr[i] += 1

def test1(np.ndarray[np.int32_t] arr):
    cdef int i
    for i in xrange(len(arr)):
        inc(<int*>arr.data, i)
