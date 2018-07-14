from github import Github
import os
import json
from functools import lru_cache
cred = json.load(open(os.path.expanduser('~/.cred/github/cred.json')))
user = cred['user']
access_token = cred['acces_token']
g = Github(user, access_token)
user = g.get_user()
_username = user.login

# no idea, just trying to cache to avoid being abusive

@lru_cache(maxsize=None)
def get_user(user):
    return g.get_user(user)

@lru_cache(maxsize=None)
def get_following(user):
    return _get_user(user).get_following()

@lru_cache(maxsize=None)
def get_followers(user):
    return _get_user(user).get_followers()
