#!/usr/bin/env python
import argh
import os

_mydir = os.path.realpath(os.path.dirname(__file__))

def run():
    pass

if __name__ == '__main__':
    argh.dispatch_command(run)
