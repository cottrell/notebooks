#!/usr/bin/env python
import argh
import os

_mydir = os.path.realpath(os.path.dirname(__file__))
_default_dir = os.path.join(_mydir, os.path.basename(__file__).rsplit('.', 1)[0])

def run():
    pass

if __name__ == '__main__':
    argh.dispatch_command(run)
