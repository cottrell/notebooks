#!/usr/bin/env python
import cloudpickle
import pdb
import pickle
import hashlib
import os
import sys
import dask
from distributed import Client
# from dask.distributed import Client
import dask.bag as db
import inspect
import traceback

from distributed import Worker
from tornado.ioloop import IOLoop
from threading import Thread
def get_repl_worker():
    loop = IOLoop.current()
    t = Thread(target=loop.start, daemon=True)
    t.start()
    w = Worker('tcp://127.0.0.1:8786', loop=loop)
    w.start()  # choose randomly assigned port
    return w

def print_and_return_message(msg):
    # for line in traceback.format_stack():
    #     print(line.strip())
    # raise Exception('something')
    return '/Users/davidcottrell/projects/notebooks/dask' in sys.path, msg

def submit(client):
    r = client.run(print_and_return_message, 'what')
    return r

def test():
    b = db.from_sequence([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    return b.map(print_and_return_message)

def cluster():
    client = Client('127.0.0.1:8786')
    return submit(client)

def local():
    # dask.set_options(get=dask.local.get_sync)
    # client = Client()
    # or
    client = Client(processes=False)
    return submit(client)

def pickletest():
    # import pdb; pdb.set_trace()
    return cloudpickle.dumps(print_and_return_message)
    # c = cloudpickle.CloudPickler(open('j', 'wb'))
    # return c.extract_func_data(print_and_return_message)

if __name__ == '__main__':
    arg = sys.argv[1]
    if arg == 'local':
        print("running local mode")
        r  = local()
        print(r)
    elif arg == 'cluster':
        print("running cluster mode")
        r = cluster()
        print(r)
    elif arg == 'pickletest':
        r = pickletest()
        print(r)
    else:
        print('no arg? {}'.format(arg))
