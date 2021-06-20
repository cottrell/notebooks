import os
import twitter
import json
cred = json.load(open(os.path.expanduser('~/.cred/twitter/cred.json')))
api = twitter.Api(**cred)

from joblib import Memory
memory = Memory('./joblib_cache_twitter_api', verbose=10)


@memory.cache
def GetFriendIDs():
    return api.GetFriendIDs()

# api = twitter.Api(**cred2)
