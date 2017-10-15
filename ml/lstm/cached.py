import os
import gzip
import pandas as pd
from functools import lru_cache
mydir = os.path.dirname(os.path.realpath(__file__))
mangled_data = os.path.join(mydir, 'mangled_data.txt.gz')
filename = os.path.join(mydir, '../../data/bis/all.text')

@lru_cache()
def get_data(filename=filename):
    if os.path.exists(mangled_data):
        print('reading {}'.format(mangled_data))
        data = gzip.open(mangled_data).read().decode()
    else:
        print('reading {}'.format(filename))
        data = open(filename).read()
        # 12 s
        s = pd.Series(list(data)).value_counts()
        # 6 s
        # keep chars with more than 1000 occurences
        a = str.maketrans({k: None for k in s[s<1000].index.tolist()})
        data = data.translate(a)
        gzip.open(mangled_data, 'w').write(data.encode())
    chars = sorted(list(set(data))) # is int if data is bytes, is str if data is str
    VOCAB_SIZE = len(chars)
    return data, chars, VOCAB_SIZE
