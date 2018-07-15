import sys
import subprocess
import os
import json
import libcache

# TODO probably hitting some paging issues

_basedir = os.path.expanduser('~/code')

def clone_following_of_followers(user=libcache._username):
    followers = libcache.get_followers(user)
    for x in followers:
        following = libcache.get_following(x['login'])
        for y in following:
            clone_user(y['login'])

def clone_followers(user=libcache._username):
    followers = libcache.get_followers(user)
    for x in followers:
        clone_user(x['login'])

def clone_user(user=libcache._username):
    """ ~/code/<user> """
    if not os.path.exists(_basedir):
        os.makedirs(_basedir)
    if not os.path.exists(os.path.join(_basedir, '.git')):
        res = run_command_get_output('cd {} && git init'.format(_basedir))
    userdir = os.path.join(_basedir, user)
    if not os.path.exists(userdir):
        os.makedirs(userdir)
        res = run_command_get_output('cd {} && git init'.format(userdir))
    all_repos = libcache.get_repos(user)
    repos = [x for x in all_repos if not x['fork'] and x['size'] > 0] # guess at how to detect empty
    print('will skip {} forks for {}'.format(len(all_repos) - len(repos), user))
    for x in all_repos:
        if x['fork']:
            print('\t{}'.format(x['full_name']))
    print('will clone {} repos for {}'.format(len(repos), user))
    for x in all_repos:
        if not x['fork']:
            print('\t{}'.format(x['full_name']))
    for x in repos:
        res = run_command_get_output('cd {} && [[ -e {} ]] || git submodule add {}'.format(userdir, x['name'], x['git_url']), do_raise=False)
        if res['status'] != 0:
            if 'You appear to have cloned an empty repository' in res['stdout']:
                pass
            else:
                raise Exception("some problem: {}".format(res))
    # for now don't fail
    res = run_command_get_output('cd {} && git submodule add ./{} || :'.format(_basedir, user))
    res = run_command_get_output('cd {} && git commit -a -m "update" || :'.format(userdir))
    res = run_command_get_output('cd {} && git commit -a -m "added {}" || : '.format(_basedir, user))

def get_followers(user=libcache._username, depth=0):
    print('get_following {} depth={}'.format(user, depth))
    d = dict()
    d[user] = list(libcache.get_followers(user))
    if depth > 0:
        for x in d[user]:
            d[x['login']] = list(get_followers(user=x['login'], depth=depth-1))
    return d

def get_following(user=libcache._username, depth=0):
    print('get_following {} depth={}'.format(user, depth))
    d = dict()
    d[user] = list(libcache.get_following(user))
    if depth > 0:
        for x in d[user]:
            d[x['login']] = list(get_following(user=x['login'], depth=depth-1))
    return d

def run_command_get_output(cmd, shell=True, splitlines=True, do_raise=True):
    print('running: {}'.format(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
    out, err = p.communicate()
    status = p.returncode
    out = out.decode()
    err = err.decode()
    if splitlines:
        out = out.split('\n')
        err = err.split('\n')
    res = dict(out=out, err=err, status=status)
    if res['status'] != 0 and do_raise:
        raise Exception('some problem: {}'.format(res))
    return res

if __name__ == '__main__':
    pass
