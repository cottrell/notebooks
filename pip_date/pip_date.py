#!/usr/bin/env python
import datetime
import hashlib
import json
import os
import pathlib

import pandas as pd
import requests
# from pip._internal.utils.misc import get_installed_distributions
 

_mydir = os.path.dirname(os.path.realpath(__file__))
_cache_dir = os.path.join(_mydir, 'cache')


# NOTE: they removed this in d051a00fc57037104fca85ad8ebf2cdbd1e32d24
from pip._internal.utils.compat import stdlib_pkgs
from typing import cast


def get_installed_distributions(
    local_only=True,
    skip=stdlib_pkgs,
    include_editables=True,
    editables_only=False,
    user_only=False,
    paths=None,
):
    """Return a list of installed Distribution objects.

    Left for compatibility until direct pkg_resources uses are refactored out.
    """
    from pip._internal.metadata import get_default_environment, get_environment
    from pip._internal.metadata.pkg_resources import Distribution as _Dist

    if paths is None:
        env = get_default_environment()
    else:
        env = get_environment(paths)
    dists = env.iter_installed_distributions(
        local_only=local_only,
        skip=skip,
        include_editables=include_editables,
        editables_only=editables_only,
        user_only=user_only,
    )
    return [cast(_Dist, dist)._dist for dist in dists]



def cached_get_json(url, expiry_seconds=60 * 60 * 24 * 30):
    # totally untested
    os.makedirs(_cache_dir, exist_ok=True)
    key = hashlib.sha1(url.encode()).hexdigest()
    filename = os.path.join(_cache_dir, key)
    path = pathlib.Path(filename)
    if path.exists():
        stat = path.stat()
        ctime = datetime.datetime.fromtimestamp(stat.st_ctime)
        dt = datetime.datetime.now() - ctime
        if dt.total_seconds() > expiry_seconds:
            path.unlink()
    if not path.exists():
        print(f'getting {url}')
        res = requests.get(url)
        assert res.ok
        json_ = res.json()
        json.dump(json_, open(filename, 'w'))
    return json.load(open(filename))


def get_info_for_packages(*names):
    out = list()
    for name in names:
        out.extend(get_info_for_package(name))
    df = pd.DataFrame(out).sort_values(['name', 'date'], ascending=[True, False])

    return df


def get_package_version_latest(*names, max_date=None):
    df = get_info_for_packages(*names)
    if max_date is not None:
        max_date = pd.to_datetime(max_date).date()
        df = df[df['date'] <= max_date]
    df = df.drop_duplicates(subset=['name'], keep='first')
    strings = (df['name'] + '==' + df['version']).tolist()
    print('')
    print('\n'.join(strings))
    print('')
    return df

def get_info_for_package(name):
    # each looks like this
    # {
    #     'comment_text': '',
    #     'digests': {'md5': '42d3775c2ece8aa9b11a1af7a423f28b',
    #      'sha256': '4d821b9b911fc1b7d428978d04ace33f0af32bb7549525c8a7b08444bce46b74'},
    #     'downloads': -1,
    #     'filename': 'pandas-1.2.3-cp37-cp37m-macosx_10_9_x86_64.whl',
    #     'has_sig': False,
    #     'md5_digest': '42d3775c2ece8aa9b11a1af7a423f28b',
    #     'packagetype': 'bdist_wheel',
    #     'python_version': 'cp37',
    #     'requires_python': '>=3.7.1',
    #     'size': 10355566,
    #     'upload_time': '2021-03-02T12:05:36',
    #     'upload_time_iso_8601': '2021-03-02T12:05:36.600299Z',
    #     'url': 'https://files.pythonhosted.org/packages/cf/6a/b662206fd22c2f9bf70793ceb2db99cf45cfaf13f11effdee45f6e5c22e1/pandas-1.2.3-cp37-cp37m-macosx_10_9_x86_64.whl',
    #     'yanked': False,
    #     'yanked_reason': None
    # }
    url = f'https://pypi.org/pypi/{name}/json'
    try:
        json_ = cached_get_json(url)
    except AssertionError as e:
        print(f'skipping {name} due to error {e}')
        return []
    versions = json_['releases']
    records = list()
    for version, details in versions.items():
        if not details:
            # some have no entries
            continue
        date = details[0]['upload_time']  # just take first
        date = pd.to_datetime(date).date()
        record = dict(name=name, version=version, date=date)
        records.append(record)
    return records


def get_installed_available():
    packages = get_installed_distributions()
    installed = list()
    for package in packages:
        name = package.name
# 2024-03-21
        installed_version = package.version
        installed.append(dict(name=name, version=installed_version))
    installed = pd.DataFrame(installed)
    available = list()
    for package in packages:
        name = package.name
        records = get_info_for_package(name)
        available.extend(records)
    available = pd.DataFrame(available)
    return installed, available


def get_info():
    df, available = get_installed_available()
    df['installed'] = True
    df = df.set_index(['name', 'version'])
    available = available.set_index(['name', 'version'])
    df = pd.concat([df, available], axis=1).reset_index().sort_values(['name', 'date'])
    df['installed'].fillna(False, inplace=True)
    df['nv'] = df.groupby('name').cumcount()
    installed = df[df.installed].drop(['installed'], axis=1).set_index('name')
    installed.columns = [f'{x}_installed' for x in installed.columns]
    av = df.drop(['installed'], axis=1).groupby('name').agg(['first', 'last'])
    av.columns = ['_'.join(x) for x in av.columns]
    df = pd.concat([installed, av], axis=1)
    df['days_behind'] = df['date_last'] - df['date_installed']
    df['releases_behind'] = df['nv_last'] - df['nv_installed']
    df = df.sort_values('days_behind')
    return df


if __name__ == '__main__':
    df = get_info()
    df.columns = pd.MultiIndex.from_tuples([x.split('_') for x in df.columns])
    df = df.sort_index(axis=1)
    print(df.to_string())
