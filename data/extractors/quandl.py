"""
No date stuff yet just pulls the bulks.
API limits are 50k calls a day on logged in free.
"""
import requests
import functools
import json
import pandas as pd
import quandl
import os
from mylib.tools import run_tasks_in_parallel
from . import lib

# _mydir, _myname, _basedir, _datadir, _metadatadir = lib.say_my_name()
# 
# for k in [_basedir, _datadir, _metadatadir]:
#     lib.mkdir_if_needed(k)
# 
# token = json.load(open(os.path.expanduser('~/.cred/quandl/auth.json')))['APIKEY']
# quandl.save_key(token)
# 
# _trim_start = '2014-01-01'
# _trim_end = '2017-01-02' # way of bumping the cache
# 
# # single sysmbol
# def get_from_quandl(code=None, trim_start=_trim_start, trim_end=_trim_end, **kwargs):
#     return quandl.get(code, trim_start=trim_start, authtoken=token, trim_end=trim_end, **kwargs).reset_index()
# 
# # library/bulk
# 
# _bulk_downloadable = ['LBMA', 'UGID', 'OECD', 'ECONOMIST', 'FRED', 'OSE', 'SHFE']
# 
# def get_all(force=False, cleanup=False):
#     dbnames = get_list()
#     tasks_meta = [functools.partial(get_metadata, k) for k in dbnames]
#     tasks_bulk = [functools.partial(get_bulk_zip, k) for k in _bulk_downloadable] # hard coded
#     tasks = tasks_meta + tasks_bulk
#     print('running {} tasks'.format(len(tasks)))
#     run_tasks_in_parallel(*tasks, max_workers=20)
# 
# 
# def get_list():
#     db = quandl.Database('')
#     a = db.all()
#     return [x.code for x in a]
# 
# 
# def get_bulk_zip(dbname, return_data=False, force=False):
#     if dbname not in _bulk_downloadable:
#         raise Exception('I do not think this is bulk downloadable {}'.format(dname))
#     # example bulk, these are bigger 43 mm lines
#     filename_zip = os.path.join(_datadir, 'raw', dbname + '.zip')
#     if not os.path.exists(filename_zip) or force:
#         print('{} does not exist'.format(filename_zip))
#         db = quandl.Database(dbname)
#         mkdir_if_needed(os.path.dirname(filename_zip))
#         db.bulk_download_to_file(filename_zip, params=dict(api_key=token))
#     else:
#         print('{} exists set force=True to repull'.format(filename_zip))
#     return filename_zip
# 
# def get_metadata(name, return_data=False, force=False, cleanup=False):
#     # no idea where this is in the api
#     filename_zip = os.path.join(_metadatadir, 'raw', name + '.zip')
#     filename = os.path.join(_metadatadir, 'parquet', name + '.parquet')
#     mkdir_if_needed(os.path.dirname(filename))
#     mkdir_if_needed(os.path.dirname(filename_zip))
#     if not os.path.exists(filename) or force:
#         print('{} does not exist'.format(filename))
#         if not os.path.exists(filename_zip) or force:
#             print('{} does not exist'.format(filename_zip))
#             url = 'https://www.quandl.com/api/v3/databases/{}/metadata?api_key={}'.format(name, token)
#             r = requests.get(url)
#             assert r.ok
#             open(filename_zip, 'wb').write(r.content)
#         else:
#             print('{} exists. set force to True to repull'.format(filename_zip))
#         df = pd.read_csv(filename_zip, compression='zip')
#         lib.try_convert_inplace(df)
#         if os.path.exists(filename):
#             lib.move_and_remove_nonblocking(filename)
#         lib.write_parquet(df, filename)
#         if cleanup:
#             lib.move_and_remove_nonblocking(filename_zip)
#     else:
#         print('{} exists. set force to True to repull'.format(filename))
#     if return_data:
#         return pd.read_parquet(filename)
# 
