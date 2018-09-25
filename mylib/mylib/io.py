"""
Stuff to do with reading and writing.
"""
import pandas
import re
import inspect
import pandas as pd
import numpy
import numpy as np
import gzip

def get_capped_line_count(filename, n=2):
    i = 0
    for x in _open(filename):
        i += 1
        if i >= n:
            break
    return i

def _open(filename, **kwargs):
    if filename.endswith('.gz'):
        return gzip.open(filename, **kwargs)
    else:
        return open(filename, **kwargs)
