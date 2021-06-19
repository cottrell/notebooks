"""
There is a python module pynytimes but is probably just as easy to simply use requests against the URL.

https://developer.nytimes.com/docs
"""
import datetime
import json
import os
import requests
from urllib.parse import urljoin, quote

_mydir = os.path.realpath(os.path.dirname(__file__))
_local_joblib_memory_dir = os.path.join(_mydir, 'joblib_cache')


# joblib cache is a bit stupid for json (it saves pkl files) but will be fast and easy). delete the joblib_cache dirs to kill cache and start fresh if you want.
from joblib import Memory
memory = Memory(_local_joblib_memory_dir, verbose=10)

# You need to set up an account manually through the web portal and then create an app, enable the apis you want and save the key in a file as below
cred = json.load(open(os.path.expanduser('~/.cred/nytimes/cred.json')))
cred = cred['archive_search_hit_datasource']

def get_pynyt_instance():
    from pynytimes import NYTAPI
    nyt = NYTAPI(cred['key'], parse_dates=True)
    # nyt = NYTAPI("Your API key", https=False)
    return nyt

BASE_URL = 'https://api.nytimes.com/svc/'

def simple_example_requests(year=2019, month=1):
    example_url = f'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={cred["key"]}'
    res = requests.get(example_url)
    assert res.ok
    return res.json()

def simple_example_pynyt(year=2019, month=1):
    nyt = get_pynyt_instance()
    return nyt.archive_metadata(datetime.datetime(year, month, 1))


@memory.cache
def article_search_requests(query='"election to election"', begin='18900101', end='19100101'):
    """Test against this location manually https://www.nytimes.com/search?dropmab=false&endDate=19100101&query=%22Election%20to%20election%22&sort=best&startDate=18910101"""
    url = urljoin(BASE_URL, f'search/v2/articlesearch.json?q={quote(query)}&begin_date={begin}&end_date={end}&api-key={cred["key"]}')
    print(f'GET: {url}')
    res = requests.get(url)
    assert res.ok
    return res.json()

