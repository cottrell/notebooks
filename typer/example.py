#!/usr/bin/env python
import typer

def this(a, *b):
    print(a, b)

if __name__ == '__main__':
    typer.run(this)
