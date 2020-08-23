#!/usr/bin/env python
import time
import requests
import os
import hashlib
import typer
import bs4
_mydir = os.path.realpath(os.path.dirname(__file__))

def run_loop(url, delay_seconds=1):
    hash_ = hashlib.sha1(url.encode()).hexdigest()
    filename = os.path.join(_mydir, hash_)
    filename_new = filename + '_new'
    print(f'Will save content to {filename}')
    old = None
    if os.path.exists(filename):
        old = open(filename).read()
    while True:
        res = requests.get(url)
        text = res.text
        if old is None:
            open(filename, 'w').write(text)
            old = text
        else:
            if old != text:
                open(filename_new, 'w').write(text)
                # just leave the file until you delete it
                while True:
                    os.system('spd-say "your program has finished"')
                    time.sleep(1)
        time.sleep(1)


if __name__ == '__main__':
    typer.run(run_loop)
