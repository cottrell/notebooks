#!/usr/bin/env python
import pickle
import hashlib
import os
import sys
import dask
from distributed import Client
# from dask.distributed import Client
import dask.bag as db

localpath = ['/Users/davidcottrell/projects/notebooks/dask/dask-worker-space/worker-fct_anr7',
 '/Users/davidcottrell/projects/notebooks/dask',
 '/Users/davidcottrell/projects/notebooks/dask',
 '/Users/davidcottrell/dev/spark-2.3.0-bin-hadoop2.7/python',
 '/Users/davidcottrell/dev/spark-2.3.0-bin-hadoop2.7/python/lib/py4j-0.10.6-src.zip',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python36.zip',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/lib-dynload',
 '/Users/davidcottrell/.local/lib/python3.6/site-packages',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/deribit_api-1.1.1-py3.6.egg',
 '/Users/davidcottrell/dev/data.world-py',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/flake8-3.4.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/tabulator-1.4.1-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/jsontableschema-0.10.1-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/configparser-3.5.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/mccabe-0.6.1-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/pycodestyle-2.3.1-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/openpyxl-2.5.0b1-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/xlrd-1.1.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/linear_tsv-1.0.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/SQLAlchemy-1.2.0b3-py3.6-macosx-10.7-x86_64.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/jsonlines-1.2.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/ijson-2.3-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/unicodecsv-0.14.1-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/cchardet-1.1.3-py3.6-macosx-10.7-x86_64.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/isodate-0.6.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/future-0.16.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/jsonschema-2.6.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/et_xmlfile-1.0.1-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/jdcal-1.3-py3.6.egg',
 '/Users/davidcottrell/dev/alpha_vantage',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/nose-1.3.7-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/simplejson-3.13.2-py3.6-macosx-10.7-x86_64.egg',
 '/Users/davidcottrell/projects/notebooks/mylib',
 '/Users/davidcottrell/dev/dateinfer',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/supervisor-4.0.0.dev0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/meld3-1.0.2-py3.6.egg',
 '/Users/davidcottrell/dev/datapackage-py',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/jsonpointer-1.14-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/rfc3986-1.1.0-py3.6.egg',
 '/Users/davidcottrell/dev/ipython',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/backcall-0.1.0-py3.6.egg',
 '/Users/davidcottrell/dev/pandas.git',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/futures-3.2.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/typing-3.6.4-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/PyVCF-0.6.8-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/oauth2client-4.1.2-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/mock-2.0.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/httplib2-0.9.2-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/hdfs-2.1.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/grpcio-1.9.1-py3.6-macosx-10.7-x86_64.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/dill-0.2.6-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/crcmod-1.7-py3.6-macosx-10.7-x86_64.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/rsa-3.4.2-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/pyasn1_modules-0.2.1-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/pbr-3.1.1-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/docopt-0.6.2-py3.6.egg',
 '/Users/davidcottrell/dev/beam3/sdks/python',
 '/Users/davidcottrell/dev/python-airmash',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/names-0.3.0-py3.6.egg',
 '/Users/davidcottrell/dev/construct',
 '/Users/davidcottrell/dev/distributed',
 '/Users/davidcottrell/dev/dask']

clusterpath = ['/Users/davidcottrell/dask-worker-space/worker-lzs3ars2',
 '/Users/davidcottrell/anaconda3/envs/363/bin',
 '/Users/davidcottrell',
 '/Users/davidcottrell/dev/spark-2.3.0-bin-hadoop2.7/python',
 '/Users/davidcottrell/dev/spark-2.3.0-bin-hadoop2.7/python/lib/py4j-0.10.6-src.zip',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python36.zip',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/lib-dynload',
 '/Users/davidcottrell/.local/lib/python3.6/site-packages',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/deribit_api-1.1.1-py3.6.egg',
 '/Users/davidcottrell/dev/data.world-py',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/flake8-3.4.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/tabulator-1.4.1-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/jsontableschema-0.10.1-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/configparser-3.5.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/mccabe-0.6.1-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/pycodestyle-2.3.1-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/openpyxl-2.5.0b1-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/xlrd-1.1.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/linear_tsv-1.0.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/SQLAlchemy-1.2.0b3-py3.6-macosx-10.7-x86_64.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/jsonlines-1.2.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/ijson-2.3-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/unicodecsv-0.14.1-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/cchardet-1.1.3-py3.6-macosx-10.7-x86_64.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/isodate-0.6.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/future-0.16.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/jsonschema-2.6.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/et_xmlfile-1.0.1-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/jdcal-1.3-py3.6.egg',
 '/Users/davidcottrell/dev/alpha_vantage',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/nose-1.3.7-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/simplejson-3.13.2-py3.6-macosx-10.7-x86_64.egg',
 '/Users/davidcottrell/projects/notebooks/mylib',
 '/Users/davidcottrell/dev/dateinfer',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/supervisor-4.0.0.dev0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/meld3-1.0.2-py3.6.egg',
 '/Users/davidcottrell/dev/datapackage-py',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/jsonpointer-1.14-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/rfc3986-1.1.0-py3.6.egg',
 '/Users/davidcottrell/dev/ipython',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/backcall-0.1.0-py3.6.egg',
 '/Users/davidcottrell/dev/pandas.git',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/futures-3.2.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/typing-3.6.4-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/PyVCF-0.6.8-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/oauth2client-4.1.2-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/mock-2.0.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/httplib2-0.9.2-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/hdfs-2.1.0-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/grpcio-1.9.1-py3.6-macosx-10.7-x86_64.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/dill-0.2.6-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/crcmod-1.7-py3.6-macosx-10.7-x86_64.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/rsa-3.4.2-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/pyasn1_modules-0.2.1-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/pbr-3.1.1-py3.6.egg',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/docopt-0.6.2-py3.6.egg',
 '/Users/davidcottrell/dev/beam3/sdks/python',
 '/Users/davidcottrell/dev/python-airmash',
 '/Users/davidcottrell/anaconda3/envs/363/lib/python3.6/site-packages/names-0.3.0-py3.6.egg',
 '/Users/davidcottrell/dev/construct',
 '/Users/davidcottrell/dev/distributed',
 '/Users/davidcottrell/dev/dask']

def get_hash(x):
    return hashlib.sha1(pickle.dumps(x)).hexdigest()

def print_and_return_message(msg):
    print("msg ".format(msg))
    path = sys.path
    diff_from_local = [x for (x, y) in zip(path, localpath) if x != y]
    diff_from_cluster = [x for (x, y) in zip(path, clusterpath) if x != y]
    return "print sys.path={}, os.getcwd()={}, sys.executable={}: {}.\ndiff_from_local={}\ndiff_from_cluster={}".format(get_hash(sys.path), os.getcwd(), sys.executable, msg, diff_from_local, diff_from_cluster)

def submit(client):
    r = client.submit(print_and_return_message, 'what')
    print("res=", r.result())
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

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'local':
        print("running local mode")
        local()
    else:
        cluster()
        print("running cluster mode")
