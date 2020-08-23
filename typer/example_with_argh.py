#!/usr/bin/env python
import argh

def this(a, *b):
    print(a, b)

if __name__ == '__main__':
    argh.dispatch_command(this)
