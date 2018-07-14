import sys
import os
import json
# pip install pygithub
import libcache

_basedir = os.path.expanduser('~/code')

# seems am throttled

def get_followers(user=libcache._username, depth=0):
    print('get_following {} depth={}'.format(user, depth))
    d = dict()
    d[user] = list(libcache.get_followers(user))
    if depth > 0:
        for x in d[user]:
            d[x.login] = list(get_followers(user=x.login, depth=depth-1))
    return d

def get_following(user=libcache._username, depth=0):
    print('get_following {} depth={}'.format(user, depth))
    d = dict()
    d[user] = list(libcache.get_following(user))
    if depth > 0:
        for x in d[user]:
            d[x.login] = list(get_following(user=x.login, depth=depth-1))
    return d

def run_command_get_output(cmd, shell=True, splitlines=True):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
    out, err = p.communicate()
    status = p.returncode
    out = out.decode()
    err = err.decode()
    if splitlines:
        out = out.split('\n')
        err = err.split('\n')
    return dict(out=out, err=err, status=status)

if __name__ == '__main__':
    pass
