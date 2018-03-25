#!/usr/bin/env python
import sys
import dask
from distributed import Client
# from dask.distributed import Client
import dask.bag as db

def print_and_return_message(msg):
    print("msg ".format(msg))
    return "print sys.path={}: {}".format(sys.path, msg)

def submit(client):
    r = client.submit(print_and_return_message, 'what')
    print("res=", r.result())

def test():
    b = db.from_sequence([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    return b.map(print_and_return_message)

def cluster():
    client = Client('127.0.0.1:8786')
    submit(client)

def local():
    # dask.set_options(get=dask.local.get_sync)
    # client = Client()
    # or
    client = Client(processes=False)
    submit(client)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'local':
        print("running local mode")
        local()
    else:
        cluster()
        print("running cluster mode")
