import requests
from github import Github # doesn't work very well, something blocking
import os
import pickle
import json
from functools import lru_cache, wraps
import atexit
from mylib.tools import tempfile_then_atomic_move
_mydir = os.path.dirname(__file__)
cred = json.load(open(os.path.expanduser('~/.cred/github/cred.json')))
user = cred['user']
access_token = cred['acces_token']
g = Github(user, access_token)
user = g.get_user()
_username = user.login

# no idea, just trying to cache to avoid being abusive

_url = 'https://api.github.com/'

class SimpleCache():
    def __init__(self, cachedir=None):
        self.cachedir = cachedir if cachedir is not None else os.path.dirname(__file__)
        self.cachefile = os.path.join(self.cachedir, 'cache.pickle')
        if os.path.exists(self.cachefile):
            print('loading {}'.format(self.cachefile))
            self._cache = pickle.load(open(self.cachefile, 'rb'))
        else:
            self._cache = dict()
        # TODO this is causing multiple runs on imp.reload
        atexit.unregister(self.save_cache)
        atexit.register(self.save_cache)
    def save_cache(self):
        with tempfile_then_atomic_move(self.cachefile) as temp:
            pickle.dump(self._cache, open(temp, 'wb'))
    def cache(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if len(kwargs) > 0:
                key = args, frozenset(kwargs.items())
            elif len(args) > 1:
                key = args
            else:
                key = args[0]
            try:
                return self._cache[key]
            except KeyError:
                self._cache[key] = result = func(*args, **kwargs)
                return result
        return wrapper

cache = SimpleCache()

@cache.cache
def get(arg):
    url = os.path.join(_url, arg)
    print('getting {}'.format(url))
    res = requests.get(url)
    return res.json()

def get_following(user):
    return get('users/{}/following'.format(user))

def get_followers(user):
    return get('users/{}/followers'.format(user))

def get_repos(user):
    return get('users/{}/repos?per_page=100'.format(user))
