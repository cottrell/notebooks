#!/usr/bin/env python
import re
import glob
import os

mydir = os.path.dirname(os.path.realpath(__file__))
def makedata():
    files = glob.glob(os.path.join(mydir, 'text/*.text'))
    fout = open(os.path.join(mydir, 'all.text'), 'w')
    reg = re.compile('\.{2,}')
    for f in files:
        print('file {}'.format(f))
        for line in open(f):
            # line = line.replace('\n', ' ')
            # line = reg.sub('', line)
            if len(line) > 10:
                fout.write(line)
        fout.write('\n')

if __name__ == '__main__':
    makedata()
