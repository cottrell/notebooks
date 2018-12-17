"""
No date stuff yet just pulls the bulks.
API limits are 50k calls a day on logged in free.
"""
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

_mydir, _myname = lib.say_my_name()

token = json.load(open(os.path.expanduser('~/.cred/quandl/auth.json')))['APIKEY']
quandl.save_key(token)

_bulk_downloadable = ['LBMA', 'UGID', 'OECD', 'ECONOMIST', 'FRED', 'OSE', 'SHFE']

def _get_bulk_args():
    pass

def _bulk_filename():
    pass

@lib.extractor(
        arg_generator=_get_bulk_args,
        filename_generator=_bulk_filename
        )
def get_quandl_bulkable(db, name, start=None, end=None):
    # get the zip, then do the thing
    filename = get_bulk_zip(db)
    # df = pd.read_csv(pd.compat.StringIO(df_str), sep=r'\s*\|\s*', engine='python')
    df = pd.read_csv(filename, compression='zip')


def get_bulk_zip(dbname, force=False):
    if dbname not in _bulk_downloadable:
        raise Exception('I do not think this is bulk downloadable {}'.format(dbname))
    # example bulk, these are bigger 43 mm lines
    filename = _zip_filename(dbname)
    if not os.path.exists(filename) or force:
        print('{} does not exist'.format(filename))
        db = quandl.Database(dbname)
        lib.mkdir_if_needed(os.path.dirname(filename))
        db.bulk_download_to_file(filename, params=dict(api_key=token))
        get_missing_headers(dname)
    else:
        print('{} exists set force=True to repull'.format(filename))
    # split TODO: move into if above
    return filename

def split_bulk_zip(filename):
    pass


def get_all_bulks_and_missing_headers():
    for k in _bulk_downloadable:
        get_bulk_zip(k)
        get_missing_headers(k) # mostly this should no-op after first setup

def get_header(ticker):
    start, end = lib.render_date_arg(start='oneweek')
    print('getting missing header for {}'.format(ticker))
    h = get_from_quandl(ticker, start=start, end=end)
    return list(h.columns)

def get_missing_headers(dbname):
    global _headers
    filename = _zip_filename(dbname)
    changed = False
    for symbol in get_symbols_from_zipfile(filename):
        ticker = '{}/{}'.format(dbname, symbol)
        if ticker not in _headers:
            _headers[ticker] = get_header(ticker)
            changed = True
    if changed:
        _dump_headers()

# single sysmbol
@ratelimit.limits(calls=50000, period=60*60*24)
def get_from_quandl(code=None, start=None, end=None, **kwargs):
    start, end = lib.render_date_arg(start, end)
    return quandl.get(code, trim_start=start, authtoken=token, trim_end=end, **kwargs).reset_index()

def _load_headers():
    global _headers
    d = json.load(open(_header_filename))
    d = dict_of_lists_to_dict(d)
    d = {k: v.split(',') for k, v in d.items()}
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
        _load_headers()()
    else:
        _headers = dict()

def get_symbols_from_zipfile(filename):
    zf = zipfile.ZipFile(filename)
    a = set()
    for y in zf.infolist():
        for x in zf.open(y):
            x = x.decode().strip().split(',', 1)[0]
            a.add(x)
    return a

def _zip_filename(dbname):
    # _tempdir = '/tmp' # tempfile.mkdtemp()
    tempdir = os.path.join(lib._basedir, 'tmp')
    lib.mkdir_if_needed(tempdir)
    # TODO: add .zip and move the files
    return os.path.join(tempdir, dbname)

def get_quandl_metadata_database(name, force=False, cleanup=False):
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
#     tasks_bulk = [functools.partial(get_bulk_zip, k) for k in _bulk_downloadable] # hard coded
#     tasks = tasks_meta + tasks_bulk
#     print('running {} tasks'.format(len(tasks)))
#     run_tasks_in_parallel(*tasks, max_workers=20)
 
 
# def get_list():
#     db = quandl.Database('')
#     a = db.all()
#     return [x.code for x in a]

