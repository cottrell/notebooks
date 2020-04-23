#!/usr/bin/env python

def mangle_data(filename=orig_data, outfile=filename):
    """ preprocessing only, do this once (manually) basically """
    if sys.version_info[0] < 3:
        raise Exception('python 2 not work')
    print('reading {}'.format(filename))
    data = gzip.open(filename).read().decode('utf-8')
    # 12 s
    s = pd.Series(list(data)).value_counts()
    # 6 s
    # keep chars with more than 1000 occurences
    a = str.maketrans({k: ' ' for k in s[s<1000].index.tolist()})
    data = data.translate(a)
    print('writing {}'.format(mangle_data))
    gzip.open(outfile, 'w').write(data.encode())

if __name__ == '__main__':
    mangle_data()
