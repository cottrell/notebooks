"""
Old stuff, probably defunct.
"""
import pandas
import re
import inspect
import pandas as pd
import numpy
import numpy as np
import pickle
import threading
import tempfile
import glob
import shutil
import logging
import json
import bcolz
import os
import time
import contextlib
import multiprocessing.pool
from pandas.core.internals import SingleBlockManager
import decorator
import functools
import gzip
from .tools import TimeLogger, AttrDict

def check_move_and_remove_and_make(path):
    if os.path.exists(path):
        move_and_remove_nonblocking(path)
    os.makedirs(path)

def move_and_remove_nonblocking(path):
    tempdir = tempfile.mkdtemp()
    logging.warning("mv %s %s && rmdir %s &" % (path, tempdir, tempdir))
    shutil.move(path, tempdir)
    threading.Thread(target=shutil.rmtree, args=[tempdir]).start()

def _to_block(d, filename, logger=None):
    if logger is None:
        logger = TimeLogger()
    with logger.timedlogger('writing {} (shape = {})'.format(filename, d.shape)):
        bcolz.carray(d, rootdir=filename)

def _to_pickle(d, filename):
    with log.timedlogger('writing {} (type={})'.format(filename, type(d))):
        pickle.dump(d, open(filename, 'wb'))

def _from_pickle(filename, logger=None):
    if logger is None:
        logger = TimeLogger()
    with logger.timedlogger('reading {}'.format(filename)):
        return pickle.load(open(filename, 'rb'))

def _from_block(filename, mode='r', logger=None):
    if logger is None:
        logger = TimeLogger()
    with logger.timedlogger('reading {}'.format(filename)):
        return bcolz.open(filename, mode=mode)

def _to_carray(s, name, path, cparams=None, format_categories=None, format_codes=None, format_values=None, logger=None):
    if logger is None:
        logger = TimeLogger()
    if type(format_categories) is str:
        format_categories = [format_categories]
    if type(format_codes) is str:
        format_codes = [format_codes]
    check_move_and_remove_and_make(path)
    meta = dict()
    meta['type'] = s.dtype.name
    meta['name'] = name

    with open(os.path.join(path, 'meta'), 'w') as fout:
        with logger.timedlogger("writing [%s] %s" % (meta['name'], fout.name)):
            print(json.dumps(meta), file=fout)

    if meta['type'] == 'category':
        categories = s.cat.categories.values
        codes = s.cat.codes.values

        if 'bcolz' in format_codes:
            rootdir = os.path.join(path, 'codes.bcolz')
            with logger.timedlogger("writing [%s] %s" % (meta['name'], rootdir)):
                bcolz.carray(codes, rootdir=rootdir, cparams=cparams)
        if 'npy' in format_codes:
            filename = os.path.join(path, 'codes.npy')
            with logger.timedlogger("writing [%s] %s" % (meta['name'], filename)):
                numpy.save(filename, codes)

        if categories.dtype == 'O':  # not robust
            categories = categories.astype(str)  # undo pandas convert to object
            # print('here', categories.dtype)
        if 'npy' in format_categories:
            filename = os.path.join(path, 'categories.npy')
            with logger.timedlogger("writing [%s] %s" % (meta['name'], filename)):
                numpy.save(filename, categories)
        if 'pickle' in format_categories:
            filename = os.path.join(path, 'categories.pickle')
            with logger.timedlogger("writing [%s] %s" % (meta['name'], filename)):
                pickle.dump(categories, open(filename, 'wb'))
        if 'npz' in format_categories:
            filename = os.path.join(path, 'categories.npz')
            with logger.timedlogger("writing [%s] %s" % (meta['name'], filename)):
                numpy.savez(filename, categories)
        if 'bcolz' in format_categories:
            rootdir = os.path.join(path, 'categories.bcolz')
            with logger.timedlogger("writing [%s] %s" % (meta['name'], rootdir)):
                bcolz.carray(categories, rootdir=rootdir, cparams=cparams)
    else:  # try
        if 'bcolz' in format_values:
            rootdir = os.path.join(path, 'values.bcolz')
            with logger.timedlogger("writing [%s] %s dtype=%s" % (meta['name'], rootdir, s.dtype)):
                bcolz.carray(s.values, rootdir=rootdir, cparams=cparams)
        if 'npy' in format_values:
            filename = os.path.join(path, 'values.npy')
            with logger.timedlogger("writing [%s] %s" % (meta['name'], filename)):
                numpy.save(filename, s.values)
        if 'pickle' in format_values:
            filename = os.path.join(path, 'values.pickle')
            with logger.timedlogger("writing [%s] %s" % (meta['name'], filename)):
                pickle.dump(s.values, open(filename, 'wb'))

def to_dict_of_things(d, path):
    check_move_and_remove_and_make(path)
    try:
        meta = {'keys': list(d.keys())}
        t = dict()
        for i, k in enumerate(meta['keys']):
            if type(d[k]) is pd.core.frame.DataFrame:
                t[k] = 'carrays'
                to_carrays(d[k], os.path.join(path, str(i)) + '.carrays')
            elif type(d[k]) in [np.ndarray, bcolz.carray_ext.carray]:
                t[k] = 'block'
                _to_block(d[k], os.path.join(path, str(i)) + '.block')
            elif type(d[k]) is pd.core.series.Series:
                raise Exception('TODO')
            else:
                t[k] = 'pickle'
                _to_pickle(d[k], os.path.join(path, str(i)) + '.pickle')
        meta['types'] = t
        json.dump(meta, open(os.path.join(path, 'meta'), 'w'))
    except Exception as e:
        logging.error("Failed creating {} for reason {}. Cleaning up.".format(path, e))
        move_and_remove_nonblocking(path)

def from_dict_of_things(path):
    meta = json.load(open(os.path.join(path, 'meta')))
    funs = {'pickle': _from_pickle,
            'carrays': from_carrays,
            'block': lambda x: _from_block(x)[:] # return numpy to avoid confusion
            }
    d = dict()
    for i, k in enumerate(meta['keys']):
        t = meta['types'][k]
        filename = os.path.join(path, '{}.{}'.format(i, t))
        d[k] = funs[t](filename)
    return d

def to_carrays(df, path, format_categories=['bcolz'], format_codes=['bcolz'], format_values=['bcolz']):
    check_move_and_remove_and_make(path)
    assert len(df.index.names) == 1
    assert df.index.names[0] is None
    for i, k in enumerate(df):
        _to_carray(df[k], k, os.path.join(path, str(i)),
                   format_categories=format_categories, format_codes=format_codes,
                   format_values=format_values)  # , cparams=bcolz.cparams(clevel=9, shuffle=True, cname='blosclz'))

def from_carrays(path, format_categories='bcolz', format_codes='bcolz', format_values='bcolz', parallel=True, logger=None):
    if logger is None:
        logger = TimeLogger()
    assert os.path.exists(path), 'No path {}'.format(path)
    df_columns = glob.glob(os.path.join(path, '*'))
    df = dict()
    if parallel:
        pool = multiprocessing.pool.ThreadPool()
        results = []
        for i, k in enumerate(df_columns):
            p = pool.apply_async(_from_carray, args=(k,), kwds={'format_categories': format_categories, 'format_codes': format_codes, 'format_values': format_values})
            results.append(p)
        pool.close()
        pool.join()
        for x in results:
            meta, s = x.get()
            df[meta['name']] = s
    else:
        for i, k in enumerate(df_columns):
            meta, s = _from_carray(k, format_categories=format_categories, format_codes=format_codes, format_values=format_values)
            df[meta['name']] = s

    # # # this is slow when we have non categoricals as series for some reason
    with logger.timedlogger('constructing dataframe from %s column dict' % len(df)):
        df = pandas.DataFrame(df)  # TODO: fast DataFrame constructor

    return df


class FakeCarrayAsNumpyArray(bcolz.carray):

    def view(self):
        return FakeCarrayAsNumpyArray(super().view())

    @property
    def flags(self):
        return AttrDict({'writeable': False})


def _from_carray(path, format_categories=None, format_codes=None, format_values=None, logger=None):
    if logger is None:
        logger = TimeLogger()
    meta = json.load(open(os.path.join(path, 'meta'), 'r'))

    if meta['type'] == 'category':
        if format_categories in ['npz', 'npy']:
            filename = os.path.join(path, 'categories.%s' % format_categories)
            with logger.timedlogger("reading [%s] %s with mmap_mode" % (meta['name'], filename)):
                categories_values = numpy.load(filename, mmap_mode='r+')  # TODO npz not memmap?
                if format_categories == 'npz':
                    categories_values = categories_values['arr_0']
        elif format_categories == 'pickle':
            filename = os.path.join(path, 'categories.pickle')
            with logger.timedlogger("reading [%s] %s" % (meta['name'], filename)):
                categories_values = pickle.load(open(filename, 'rb'))
        elif format_categories == 'bcolz':
            rootdir = os.path.join(path, 'categories.bcolz')
            with logger.timedlogger("reading [%s] %s" % (meta['name'], rootdir)):
                categories_values = FakeCarrayAsNumpyArray(rootdir=rootdir, mode='r')
                # categories_values = bcolz.carray(rootdir=rootdir, mode='r')[:]
        else:
            raise NotImplementedError("uh oh %s" % (meta['type'],))

        if format_codes == 'bcolz':
            rootdir = os.path.join(path, 'codes.bcolz')
            with logger.timedlogger("reading [%s] %s" % (meta['name'], rootdir)):
                codes_values = bcolz.open(rootdir=rootdir, mode='r')[:]  # , categories=categories_values)
                # codes_values = FakeCarrayAsNumpyArray(rootdir=rootdir, mode='r') # , categories=categories_values)
        elif format_codes == 'npy':
            filename = os.path.join(path, 'codes.npy')
            with logger.timedlogger("reading [%s] %s with mmap_mode" % (meta['name'], filename)):
                codes_values = numpy.load(filename, mmap_mode='r+')
        else:
            raise Exception("unknown format_codes type %s" % (format_codes,))

        with logger.timedlogger("FastCat construction"):
            s = FastCat(codes_values, categories_values)
    else:
        if format_values == 'bcolz':
            rootdir = os.path.join(path, 'values.bcolz')
            with logger.timedlogger("reading [%s] %s" % (meta['name'], rootdir)):
                # values = FakeCarrayAsNumpyArray(rootdir=rootdir, mode='r')
                s = bcolz.open(rootdir=rootdir, mode='r')[:]
        elif format_values == 'npy':
            filename = os.path.join(path, 'values.npy')
            with logger.timedlogger("reading [%s] %s with mmap_mode" % (meta['name'], filename)):
                s = numpy.load(filename, mmap_mode='r+')
        elif format_values == 'pickle':
            filename = os.path.join(path, 'values.pickle')
            with logger.timedlogger("reading [%s] %s with mmap_mode" % (meta['name'], filename)):
                s = pickle.load(open(filename, 'rb'))
        # with logger.timedlogger("FastSeries construction"):
        #     index = pandas.Index(numpy.arange(len(values)), copy=False)
        #     values = SingleBlockManager(values, index, fastpath=True)
        #     s = pandas.Series(data=values, fastpath=True, copy=False, dtype=meta['type'])
        # s = values # [:]
    # logging.warning('Constructing categorical for %s' % meta['name'])
    # s = pandas.Categorical.from_codes(codes_values, categories_values, name=meta['name'])
    if isinstance(meta['name'], list):
        meta['name'] = tuple(meta['name'])
    return meta, s  # codes_values, categories_values

class FastCat(pandas.Categorical):

    def __init__(self, codes, categories, ordered=False):
        self._categories = None
        self._codes = None
        self.set_cod(codes)
        self.set_cat(categories, ordered)

    def set_cod(self, codes):
        self._codes = codes  # [:]
    def set_cat(self, categories, ordered):
        # self._categories = self._validate_categories(categories)
        self._categories = pandas.Index(categories)
        self._ordered = ordered
