"""
No date stuff yet just pulls the bulks.
API limits are 50k calls a day on logged in free.
"""
from io import StringIO
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
from . import lib
import tempfile

_mydir, _myname = lib.say_my_name()

token = json.load(open(os.path.expanduser('~/.cred/quandl/auth.json')))['APIKEY']
quandl.save_key(token)

_bulk_downloadable = ['LBMA', 'UGID', 'OECD', 'ECONOMIST', 'FRED', 'OSE', 'SHFE']

# TODO: UGID
# TODO: apply schemas see pdr

# NOTES:
# FRED has about 339k symbols. 43 mm rows.
# OECD has about 1mm symbols. 30 mm rows.
# LBMA and UGID are irregular and need a special pattern
# the otheres are tiny


@lib.extractor(partition_cols=['bucket'])
def get_fred(start=None, end=None, force=False, chunksize=1000000):
    return _get_bulk('FRED', start=start, end=end, chunksize=chunksize, force=force)

@lib.extractor(partition_cols=['bucket'])
def get_oecd(start=None, end=None, chunksize=10000000):
    return _get_bulk('OECD', start=start, end=end, chunksize=chunksize)

def _get_bulk(db, start=None, end=None, force=False, chunksize=1000000):
    assert db in {'FRED', 'OECD'}
    filename = _get_bulk_zip(db, force=force) # should be no op, force to repull
    # 43 mm / 32 is about 1-2 mm rows in each bucket
    bucketizer = lambda df: pd.util.hash_pandas_object(df['symbol'], index=False).mod(32)
    # TODO consider bucket by YEAR?
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


def _log_bad_symbol(db, symbol):
    fout = open(os.path.join(_mydir, 'bad_symbols.txt'), 'w')
    fout.write('{}/{}'.format(db, symbol))
    fout.close()

@lib.extractor(
        # partition_cols=['symbol'],
        clearable=True)
def get_ugid(start=None, end=None, force=False):
    # DO NOT DO THIS IT IS TOO CHOPPY NEED TO AGG BEFORE WRITE. What did I mean?
    db = 'UGID'
    filename = _get_bulk_zip(db, force=force) # should be no op, force to repull
    print('reading {}'.format(filename))
    def read_to_df(a, symbol):
        a.seek(0)
        df = pd.read_csv(a, header=None)
        # df = df.drop(0, axis=1)
        cols = ['symbol'] + _headers['{}/{}'.format(db, symbol)]
        if df.shape[1] != len(cols):
            print("problem with col shape of {}/{}. using generic columns".format(db, symbol))
            _log_bad_symbol(db, symbol)
            cols = ['symbol', 'date'] + ['col_{:02d}'.format(i) for i in range(df.shape[1] - 2)]
        df.columns = cols
        s = df.set_index(['symbol', 'date']).stack().reset_index()
        s.columns = ['symbol', 'date', 'feature', 'value']
        return s
    zf = zipfile.ZipFile(filename)
    # this will likely be pretty slow in python
    symbol_last = None
    a = StringIO()
    dfs = list()
    write_every_n = 1000
    for y in zf.infolist():
        for x in zf.open(y):
            x = x.decode()
            symbol = x.split(',', 1)[0]
            if (symbol_last is not None) and (symbol_last != symbol):
                try:
                    dfs.append(read_to_df(a, symbol_last))
                except ValueError as e:
                    raise e
                    print('problem with {}. skipping'.format(symbol_last))
                    _log_bad_symbol(db, symbol_last)
                a = StringIO() # reset regardless
            a.write(x)
            symbol_last = symbol
            if len(dfs) >= 1000:
                df = pd.concat(dfs, axis=0)
                yield {}, df
                dfs = list()
    a.seek(0)
    dfs.append(read_to_df(a, symbol_last))
    df = pd.concat(dfs, axis=0)
    yield {}, df

@lib.extractor(partition_cols=['symbol'], clearable=True)
def get_lbma(start=None, end=None, force=False):
    db = 'LBMA'
    filename = _get_bulk_zip(db, force=force) # should be no op, force to repull
    print('reading {}'.format(filename))
    def read_to_df(a, symbol):
        a.seek(0)
        df = pd.read_csv(a, header=None)
        df = df.drop(0, axis=1)
        df.columns = _headers['{}/{}'.format(db, symbol)]
        s = df.set_index(['date']).stack().reset_index()
        s.columns = ['date', 'feature', 'value']
        return {'symbol': symbol}, s
    zf = zipfile.ZipFile(filename)
    # this will likely be pretty slow in python
    symbol_last = None
    a = StringIO()
    for y in zf.infolist():
        for x in zf.open(y):
            x = x.decode()
            symbol = x.split(',', 1)[0]
            if (symbol_last is not None) and (symbol_last != symbol):
                yield read_to_df(a, symbol_last)
                a = StringIO()
            a.write(x)
            symbol_last = symbol
    a.seek(0)
    yield read_to_df(a, symbol_last)

@lib.extractor(clearable=True)
def get_shfe(start=None, end=None, force=False):
    db = 'SHFE'
    filename = _get_bulk_zip(db, force=force) # should be no op, force to repull
    print('reading {}'.format(filename))
    df = pd.read_csv(filename, compression='zip', header=None)
    df.columns = _headers[db]
    yield {}, df

@lib.extractor(clearable=True)
def get_ose(start=None, end=None, force=False):
    db = 'OSE'
    filename = _get_bulk_zip(db, force=force) # should be no op, force to repull
    columns = _headers[db]
    print('reading {}'.format(filename))
    # no idea why we need usecols, it was erroring with header=None
    df = pd.read_csv(filename, compression='zip', header=None, usecols=range(10))
    df.columns = _headers[db]
    yield {}, df

@lib.extractor(clearable=True)
def get_economist(start=None, end=None, force=False):
    db = 'ECONOMIST'
    filename = _get_bulk_zip(db, force=force) # should be no op, force to repull
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
        if force:
            print('{} forced'.format(filename))
        else:
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
            symbol = x.split(b',', 1)[0]
            # .split(b'_')[0]
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
    d = lib.dict_of_lists_to_dict(d)
    d = {k: v.lower().split(',') for k, v in d.items()}
    _headers = d

def _dump_headers():
    print('saving headers')
    d = {k: ','.join(v) for k, v in _headers.items()}
    d = lib.invert_dict(d)
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

def get_header(ticker):
    global _headers
    start, end = lib.render_date_arg(start='oneweek')
    print('getting missing header for {}'.format(ticker))
    h = get_from_quandl(ticker, start=start, end=end)
    c = list(h.columns)
    _headers[ticker] = c
    return c
