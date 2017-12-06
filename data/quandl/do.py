import json
import quandl
import os

mydir = os.path.dirname(os.path.realpath(__file__))

token = json.load(open(os.path.expanduser('~/.cred/quandl/auth.json')))['APIKEY']
_trim_start = '2014-01-01'
_trim_end = '2017-01-02' # way of bumping the cache

def get_from_quandl(code=None, trim_start=_trim_start, trim_end=_trim_end, **kwargs):
    return quandl.get(code, trim_start=trim_start, authtoken=token, trim_end=trim_end, **kwargs).reset_index()
