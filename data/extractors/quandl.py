"""
No date stuff yet just pulls the bulks.
API limits are 50k calls a day on logged in free.
"""
import concurrent
import gzip
import zipfile
import requests
import functools
import ratelimit
import json
import pandas as pd
import quandl
import os
from mylib.tools import run_tasks_in_parallel, run_command_get_output, dict_of_lists_to_dict, invert_dict
from . import lib
import tempfile
from mylib import bok, wok

_mydir, _myname = lib.say_my_name()

token = json.load(open(os.path.expanduser('~/.cred/quandl/auth.json')))['APIKEY']
quandl.save_key(token)

_bulk_downloadable = ['LBMA', 'UGID', 'OECD', 'ECONOMIST', 'FRED', 'OSE', 'SHFE']

# TODO: LBMA AND UGID

# NOTES:
# FRED has about 339k symbols. 43 mm rows.
# OECD has about 1mm symbols. 30 mm rows.
# LBMA and UGID are irregular and need a special pattern
# the otheres are tiny


@lib.extractor(partition_cols=['bucket'])
def get_fred(start=None, end=None, chunksize=1000000):
    return _get_bulk('FRED', start=start, end=end, chunksize=chunksize)

@lib.extractor(partition_cols=['bucket'])
def get_oecd(start=None, end=None, chunksize=10000000):
    return _get_bulk('OECD', start=start, end=end, chunksize=chunksize)

def _get_bulk(db, start=None, end=None, chunksize=1000000):
    assert db in {'FRED', 'OECD'}
    filename = _get_bulk_zip(db) # should be no op, force to repull
    # 43 mm / 32 is about 1-2 mm rows in each bucket
    bucketizer = lambda df: pd.util.hash_pandas_object(df['symbol'], index=False).mod(32)
    columns = _headers[db]
    print('reading {}'.format(filename))
    if chunksize is None:
        df = pd.read_csv(filename, compression='zip', header=None)
        df.columns = columns
        df['bucket'] = bucketizer(df)
        yield {'db': db}, df
    else:
        for df in pd.read_csv(filename, compression='zip', chunksize=chunksize, header=None):
            df.columns = columns
            df['bucket'] = bucketizer(df)
            yield {'db': db}, df

@lib.extractor(clearable=True)
def get_shfe(start=None, end=None):
    db = 'SHFE'
    filename = _get_bulk_zip(db) # should be no op, force to repull
    print('reading {}'.format(filename))
    df = pd.read_csv(filename, compression='zip', header=None)
    df.columns = _headers[db]
    yield {}, df

@lib.extractor(clearable=True)
def get_ose(start=None, end=None):
    db = 'OSE'
    filename = _get_bulk_zip(db) # should be no op, force to repull
    columns = _headers[db]
    print('reading {}'.format(filename))
    # no idea why we need usecols, it was erroring with header=None
    df = pd.read_csv(filename, compression='zip', header=None, usecols=range(10))
    df.columns = _headers[db]
    yield {}, df

@lib.extractor(clearable=True)
def get_economist(start=None, end=None):
    db = 'ECONOMIST'
    filename = _get_bulk_zip(db) # should be no op, force to repull
    print('reading {}'.format(filename))
    df = pd.read_csv(filename, compression='zip', header=None)
    df.columns = _headers[db]
    yield {}, df






def _get_bulk_zip(dbname, force=False):
    if dbname not in _bulk_downloadable:
        raise Exception('I do not think this is bulk downloadable {}'.format(dbname))
    # example bulk, these are bigger 43 mm lines
    filename = _zip_filename(dbname)
    if not os.path.exists(filename) or force:
        print('{} does not exist'.format(filename))
        db = quandl.Database(dbname)
        lib.mkdir_if_needed(os.path.dirname(filename))
        db.bulk_download_to_file(filename, params=dict(api_key=token))
    else:
        print('{} exists set force=True to repull'.format(filename))
    return filename

def split_bulk_zip(filename):
    """Split the bulk file into separate chunks by part of symbol.
    Best guess at the moment. Even the column data appears to be messed up.
    currenly always override

    ONLY DO THIS FOR LBMA or UGID.
    """
    print('splitting {}'.format(filename))
    assert filename.endswith('.zip')
    dirname = filename[:-4]
    if os.path.exists(dirname):
        lib.move_to_trash(dirname)
    lib.mkdir_if_needed(dirname)
    zf = zipfile.ZipFile(filename)
    # this will likely be pretty slow in python
    symbol_last = ''
    for y in zf.infolist():
        for x in zf.open(y):
            symbol = x.split(b',', 1)[0].split(b'_')[0]
            if symbol_last != symbol:
                outfile = os.path.join(dirname, symbol.decode())
                print('opening {}'.format(outfile))
                writer = open(outfile, 'ab')
            writer.write(x)
            symbol_last = symbol

def open_zipfile(filename):
    zf = zipfile.ZipFile(filename)
    for y in zf.infolist():
        for x in zf.open(y):
            yield x

# single sysmbol
@ratelimit.limits(calls=50000, period=60*60*24)
def get_from_quandl(code=None, start=None, end=None, **kwargs):
    start, end = lib.render_date_arg(start, end)
    return quandl.get(code, trim_start=start, authtoken=token, trim_end=end, **kwargs).reset_index()

def _load_headers():
    global _headers
    d = json.load(open(_header_filename))
    d = dict_of_lists_to_dict(d)
    d = {k: v.lower().split(',') for k, v in d.items()}
    _headers = d

def _dump_headers():
    print('saving headers')
    d = {k: ','.join(v) for k, v in _headers.items()}
    d = invert_dict(d)
    json.dump(d, open(_header_filename, 'w'), indent=4, sort_keys=True)

_header_filename = os.path.join(_mydir, 'headers.json')
try:
    _headers
except NameError as e:
    if os.path.exists(_header_filename):
        _load_headers()
    else:
        _headers = dict()

def _zip_filename(dbname):
    # _tempdir = '/tmp' # tempfile.mkdtemp()
    tempdir = os.path.join(lib._basedir, 'tmp')
    lib.mkdir_if_needed(tempdir)
    return os.path.join(tempdir, dbname) + '.zip'

def get_metadata_database(name, force=False, cleanup=False):
    # no idea where this is in the api
    filename_zip = _zip_filename('metadata_database_{}'.format(name))
    lib.mkdir_if_needed(os.path.dirname(filename_zip))
    if not os.path.exists(filename_zip) or force:
        print('{} does not exist'.format(filename_zip))
        url = 'https://www.quandl.com/api/v3/databases/{}/metadata?api_key={}'.format(name, token)
        r = requests.get(url)
        assert r.ok
        open(filename_zip, 'wb').write(r.content)
    else:
        print('{} exists. set force to True to repull'.format(filename_zip))
    # zf = zipfile.ZipFile(filename_zip)
    # d = json.load(zf.open(zf.infolist()[0]))
    df = pd.read_csv(filename_zip, compression='zip')
    lib.try_convert_inplace(df)
    if cleanup:
        lib.move_and_remove_nonblocking(filename_zip)
    return df


# def get_all(force=False, cleanup=False):
#     dbnames = get_list()
#     tasks_meta = [functools.partial(get_metadata, k) for k in dbnames]
#     tasks_bulk = [functools.partial(_get_bulk_zip, k) for k in _bulk_downloadable] # hard coded
#     tasks = tasks_meta + tasks_bulk
#     print('running {} tasks'.format(len(tasks)))
#     run_tasks_in_parallel(*tasks, max_workers=20)
 
 
# def get_list():
#     db = quandl.Database('')
#     a = db.all()
#     return [x.code for x in a]

# column analysis
# In [34]: set(map(lambda x: (x.split(b',', 1)[0], x.find(b',')),  q.open_zipfile(os.path.expanduser('~/projects/data/tmp/LBMA.zip'))))
# Out[34]: {(b'DAILY', 5), (b'GOFO', 4), (b'GOLD', 4), (b'SILVER', 6)}

# UGID is all over the place
# In [38]: a = set(map(lambda x: (x.split(b',', 1)[0], x.find(b',')),  q.open_zipfile(os.path.expanduser('~/projects/data/tmp/UGID.zip'))))
# In [39]: len(a)
# Out[39]: 8831

# def get_all_bulks_and_missing_headers(max_workers=10):
#     executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
#     fut = list()
#     for k in _bulk_downloadable:
#         filename = _get_bulk_zip(k)
#         if k in ['LBMA', 'UGID']:
#             split_bulk_zip(filename)
#             # fut.append(executor.submit(split_bulk_zip, filename))
#             # seems like only LBMA AND UGID have varying cols
#             get_missing_headers(k) # mostly this should no-op after first setup
#     res = [x.result() for x in fut]

# def get_header(ticker):
#     start, end = lib.render_date_arg(start='oneweek')
#     print('getting missing header for {}'.format(ticker))
#     h = get_from_quandl(ticker, start=start, end=end)
#     return list(h.columns)

# def get_missing_headers(dbname):
#     global _headers
#     filename = _zip_filename(dbname)
#     if dbname in ['LBMA', 'UGID']:
#         changed = False
#         for symbol in get_symbols_from_zipfile(filename):
#             ticker = '{}/{}'.format(dbname, symbol)
#             if ticker not in _headers:
#                 _headers[ticker] = get_header(ticker)
#                 changed = True
#     else:
#         if dbname not in _headers:
#             # else, get first ticker and assume all cols are the same
#             for symbol in get_symbols_from_zipfile(filename):
#                 break
#             ticker = '{}/{}'.format(dbname, symbol)
#             print('geting one header from {} for all of {}'.format(ticker, dbname))
#             print("PROBABLY BEST TO GET THE HEADERS MANUALLY!")
#             _headers[dbname] = get_header(ticker)
#             changed = True
#     if changed:
#         print('updating missing headers for {}'.format(dbname))
#         _dump_headers()
#     else:
#         print('no missing headers for {}'.format(dbname))


# def get_symbols_from_zipfile(filename):
#     zf = zipfile.ZipFile(filename)
#     a = set()
#     for y in zf.infolist():
#         for x in zf.open(y):
#             x = x.decode().strip().split(',', 1)[0]
#             a.add(x)
#     return a
