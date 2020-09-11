#!/usr/bin/env python
import typer
from corelib.util.typer import make_app

def this(a, b=1):
    print(a, b)

def that(a, b=2):
    print(a, b)

if __name__ == '__main__':
    app = make_app(this, that)
    app()
