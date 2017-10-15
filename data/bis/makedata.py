#!/usr/bin/env python
import glob
import os

mydir = os.path.dirname(os.path.realpath(__file__))
def makedata():
    files = glob.glob(os.path.join(mydir, 'text/*.text'))
    fout = open(os.path.join(mydir, 'all.text'), 'w')
    for f in files:
        for line in open(f):
            line = line.strip()
            if len(line) > 10:
                fout.write(line)

if __name__ == '__main__':
    makedata()
