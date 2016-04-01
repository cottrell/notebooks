import pandas
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

class TimeLogger():

    def __init__(self, log=logging.warning):
        self.d = dict()
        self.log = log

    @contextlib.contextmanager
    def timedlogger(self, *name):
        start = time.time()
        # self.log("%s ..." % (name,))
        yield
        end = time.time()
        interval = end - start
        self.log("%f s : %s " % (interval, '-'.join(name)))
        self.d[name] = [start, end, interval]

    def get_frame(self):
        return pandas.DataFrame(self.d, index=['start', 'stop', 'ellapsed']).T

    def clear(self):
        self.d = dict()


log = TimeLogger()

def cachecalc(path=None):
    """ basic bundler and serializer of dict outputs. Tries to use **kwargs using default_namer (*args is banned). """

    def default_namer(**kwargs):
        """ try best attempt make a name """
        return ['{}={}'.format(k, kwargs[k]) for k in sorted(kwargs.keys())]

    def inner(fun, **kwargs):
        _path = path
        d = fun(**kwargs)
        if _path is None:
            _path = '_'.join([fun.__name__] + default_namer(**kwargs)) + '.things' # save locally, could get weird with this default
        if hasattr(_path, '__call__'):
            _path = _path(**kwargs)
        assert type(_path) is str
        if os.path.exists(_path):
            logging.warning("reading from cache {}".format(_path))
            d = from_dict_of_things(_path)
        else:
            logging.warning("Computing new {}".format(_path))
            d = fun(**kwargs)
            to_dict_of_things(d, _path)
        return d
    return decorator.decorator(inner)

def to_dict_of_things(d, path):
    if os.path.exists(path):
        _move_and_remove_nonblocking(path)
    _mkdir(path)
    try:
        meta = {'keys': list(d.keys())}
        t = dict()
        for i, k in enumerate(meta['keys']):
            if type(d[k]) is pd.core.frame.DataFrame:
                t[k] = 'carrays'
                to_carrays(d[k], os.path.join(path, str(i)) + '.carrays')
            elif type(d[k]) in [np.ndarray, bcolz.carray_ext.carray]:
                t[k] = 'block'
                to_block(d[k], os.path.join(path, str(i)) + '.block')
            elif type(d[k]) is pd.core.series.Series:
                raise Exception('TODO')
            else:
                t[k] = 'pickle'
                to_pickle(d[k], os.path.join(path, str(i)) + '.pickle')
        meta['types'] = t
        json.dump(meta, open(os.path.join(path, 'meta'), 'w'))
    except Exception as e:
        logging.error("Failed creating {} for reason {}. Cleaning up.".format(path, e))
        _move_and_remove_nonblocking(path)

def from_dict_of_things(path):
    meta = json.load(open(os.path.join(path, 'meta')))
    funs = {'pickle': from_pickle,
            'carrays': from_carrays,
            'block': lambda x: from_block(x)[:] # return numpy to avoid confusion
            }
    d = dict()
    for i, k in enumerate(meta['keys']):
        t = meta['types'][k]
        filename = os.path.join(path, '{}.{}'.format(i, t))
        d[k] = funs[t](filename)
    return d

def to_pickle(d, filename):
    with log.timedlogger('writing {} (type = {})'.format(filename, type(d))):
        pickle.dump(d, open(filename, 'wb'))

def to_block(d, filename):
    with log.timedlogger('writing {} (shape = {})'.format(filename, d.shape)):
        bcolz.carray(d, rootdir=filename)

def to_carrays(df, path, format_categories=['bcolz'], format_codes=['bcolz'], format_values=['bcolz']):
    # using format_categories as list for testing
    # TODO: appears to be bug or problem with bcolz categories blowing up in storage
    if os.path.exists(path):
        _move_and_remove_nonblocking(path)  # TODO move/raise only
    _mkdir(path)
    for i, k in enumerate(df):
        _to_carray(df[k], k, os.path.join(path, str(i)),
                   format_categories=format_categories, format_codes=format_codes,
                   format_values=format_values)  # , cparams=bcolz.cparams(clevel=9, shuffle=True, cname='blosclz'))

def from_pickle(filename):
    with log.timedlogger('reading {}'.format(filename)):
        return pickle.load(open(filename, 'rb'))

def from_block(filename, mode='r'):
    with log.timedlogger('reading {}'.format(filename)):
        return bcolz.open(filename, mode=mode)

def from_carrays(path, format_categories='bcolz', format_codes='bcolz', format_values='bcolz', parallel=True):
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
    with log.timedlogger('constructing dataframe from %s column dict' % len(df)):
        df = pandas.DataFrame(df)  # TODO: fast DataFrame constructor

    return df


def _to_carray(s, name, path, cparams=None, format_categories=None, format_codes=None, format_values=None):
    if type(format_categories) is str:
        format_categories = [format_categories]
    if type(format_codes) is str:
        format_codes = [format_codes]
    if os.path.exists(path):
        _move_and_remove_nonblocking(path)
    _mkdir(path)
    meta = dict()
    meta['type'] = s.dtype.name
    meta['name'] = name

    with open(os.path.join(path, 'meta'), 'w') as fout:
        with log.timedlogger("writing [%s] %s" % (meta['name'], fout.name)):
            print(json.dumps(meta), file=fout)

    if meta['type'] == 'category':
        categories = s.cat.categories.values
        codes = s.cat.codes.values

        if 'bcolz' in format_codes:
            rootdir = os.path.join(path, 'codes.bcolz')
            with log.timedlogger("writing [%s] %s" % (meta['name'], rootdir)):
                bcolz.carray(codes, rootdir=rootdir, cparams=cparams)
        if 'npy' in format_codes:
            filename = os.path.join(path, 'codes.npy')
            with log.timedlogger("writing [%s] %s" % (meta['name'], filename)):
                numpy.save(filename, codes)

        if categories.dtype == 'O':  # not robust
            categories = categories.astype(str)  # undo pandas convert to object
            # print('here', categories.dtype)
        if 'npy' in format_categories:
            filename = os.path.join(path, 'categories.npy')
            with log.timedlogger("writing [%s] %s" % (meta['name'], filename)):
                numpy.save(filename, categories)
        if 'pickle' in format_categories:
            filename = os.path.join(path, 'categories.pickle')
            with log.timedlogger("writing [%s] %s" % (meta['name'], filename)):
                pickle.dump(categories, open(filename, 'wb'))
        if 'npz' in format_categories:
            filename = os.path.join(path, 'categories.npz')
            with log.timedlogger("writing [%s] %s" % (meta['name'], filename)):
                numpy.savez(filename, categories)
        if 'bcolz' in format_categories:
            rootdir = os.path.join(path, 'categories.bcolz')
            with log.timedlogger("writing [%s] %s" % (meta['name'], rootdir)):
                bcolz.carray(categories, rootdir=rootdir, cparams=cparams)
    else:  # try
        if 'bcolz' in format_values:
            rootdir = os.path.join(path, 'values.bcolz')
            with log.timedlogger("writing [%s] %s dtype=%s" % (meta['name'], rootdir, s.dtype)):
                bcolz.carray(s.values, rootdir=rootdir, cparams=cparams)
        if 'npy' in format_values:
            filename = os.path.join(path, 'values.npy')
            with log.timedlogger("writing [%s] %s" % (meta['name'], filename)):
                numpy.save(filename, s.values)
        if 'pickle' in format_values:
            filename = os.path.join(path, 'values.pickle')
            with log.timedlogger("writing [%s] %s" % (meta['name'], filename)):
                pickle.dump(s.values, open(filename, 'wb'))


class AttrDict(dict):

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class FakeCarrayAsNumpyArray(bcolz.carray):

    def view(self):
        return FakeCarrayAsNumpyArray(super().view())

    @property
    def flags(self):
        return AttrDict({'writeable': False})


def _from_carray(path, format_categories=None, format_codes=None, format_values=None):
    meta = json.load(open(os.path.join(path, 'meta'), 'r'))

    if meta['type'] == 'category':
        if format_categories in ['npz', 'npy']:
            filename = os.path.join(path, 'categories.%s' % format_categories)
            with log.timedlogger("reading [%s] %s with mmap_mode" % (meta['name'], filename)):
                categories_values = numpy.load(filename, mmap_mode='r+')  # TODO npz not memmap?
                if format_categories == 'npz':
                    categories_values = categories_values['arr_0']
        elif format_categories == 'pickle':
            filename = os.path.join(path, 'categories.pickle')
            with log.timedlogger("reading [%s] %s" % (meta['name'], filename)):
                categories_values = pickle.load(open(filename, 'rb'))
        elif format_categories == 'bcolz':
            rootdir = os.path.join(path, 'categories.bcolz')
            with log.timedlogger("reading [%s] %s" % (meta['name'], rootdir)):
                categories_values = FakeCarrayAsNumpyArray(rootdir=rootdir, mode='r')
                # categories_values = bcolz.carray(rootdir=rootdir, mode='r')[:]
        else:
            raise NotImplementedError("uh oh %s" % (meta['type'],))

        if format_codes == 'bcolz':
            rootdir = os.path.join(path, 'codes.bcolz')
            with log.timedlogger("reading [%s] %s" % (meta['name'], rootdir)):
                codes_values = bcolz.open(rootdir=rootdir, mode='r')[:]  # , categories=categories_values)
                # codes_values = FakeCarrayAsNumpyArray(rootdir=rootdir, mode='r') # , categories=categories_values)
        elif format_codes == 'npy':
            filename = os.path.join(path, 'codes.npy')
            with log.timedlogger("reading [%s] %s with mmap_mode" % (meta['name'], filename)):
                codes_values = numpy.load(filename, mmap_mode='r+')
        else:
            raise Exception("unknown format_codes type %s" % (format_codes,))

        with log.timedlogger("FastCat construction"):
            s = FastCat(codes_values, categories_values)
    else:
        if format_values == 'bcolz':
            rootdir = os.path.join(path, 'values.bcolz')
            with log.timedlogger("reading [%s] %s" % (meta['name'], rootdir)):
                # values = FakeCarrayAsNumpyArray(rootdir=rootdir, mode='r')
                s = bcolz.open(rootdir=rootdir, mode='r')[:]
        elif format_values == 'npy':
            filename = os.path.join(path, 'values.npy')
            with log.timedlogger("reading [%s] %s with mmap_mode" % (meta['name'], filename)):
                s = numpy.load(filename, mmap_mode='r+')
        elif format_values == 'pickle':
            filename = os.path.join(path, 'values.pickle')
            with log.timedlogger("reading [%s] %s with mmap_mode" % (meta['name'], filename)):
                s = pickle.load(open(filename, 'rb'))
        # with log.timedlogger("FastSeries construction"):
        #     index = pandas.Index(numpy.arange(len(values)), copy=False)
        #     values = SingleBlockManager(values, index, fastpath=True)
        #     s = pandas.Series(data=values, fastpath=True, copy=False, dtype=meta['type'])
        # s = values # [:]
    # logging.warning('Constructing categorical for %s' % meta['name'])
    # s = pandas.Categorical.from_codes(codes_values, categories_values, name=meta['name'])
    return meta, s  # codes_values, categories_values


@contextlib.contextmanager
def timedlogger(name, log=logging.warning):
    start = time.time()
    log("%s ..." % name)
    yield
    end = time.time()
    interval = end - start
    log("%f s : %s " % (interval, name))


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


def _mkdir(path):
    logging.warning("mkdir %s" % path)
    os.mkdir(path)


def _move_and_remove_nonblocking(path):
    tempdir = tempfile.mkdtemp()
    logging.warning("mv %s %s && rmdir %s &" % (path, tempdir, tempdir))
    shutil.move(path, tempdir)
    threading.Thread(target=shutil.rmtree, args=[tempdir]).start()


def _rmdir(path):
    logging.warning("rmdir %s" % path)
    shutil.rmtree(path)

################################################################################
def from_dict_of_blocks(rootdir, mode='r'):
    """ deprecated """
    meta = json.load(open(os.path.join(rootdir, 'meta')))
    d = dict()
    for i, k in enumerate(meta['keys']):
        filename = os.path.join(rootdir, str(i))
        with log.timedlogger('reading {} ({})'.format(filename, k)):
            d[k] = bcolz.open(filename, mode=mode)
            print('... d[{}].shape = {}'.format(k, d[k].shape))
    return d

def to_dict_of_blocks(d, rootdir):
    """ deprecated. for pure numpy things like {'X_train': X_train, 'X_test': X_test} """
    if os.path.exists(rootdir):
        _move_and_remove_nonblocking(rootdir)
    _mkdir(rootdir)
    meta = {'keys': list(d.keys())}
    json.dump(meta, open(os.path.join(rootdir, 'meta'), 'w'))
    for i, k in enumerate(meta['keys']):
        filename = os.path.join(rootdir, str(i))
        with log.timedlogger('writing {} ({}.shape = {})'.format(filename, k, d[k].shape)):
            bcolz.carray(d[k], rootdir=filename)



# ######################
# def get_carray_monkeypatched(rootdir=None, categories=None):
#     class carray(bcolz.carray):
#         self.flags = None
#     ca = carray(rootdir=rootdir)
#     ca.max = lambda : len(categories) - 1
#     ca.min = lambda : 0
#     return ca
#
# def fast_cat_constructor(codes, categories, ordered=False):
#     c = pandas.Categorical(codes, categories=categories, ordered=False,
#             use_values_as_codes_directly=True)
#     # c = pandas.Categorical([], categories=None)
#     # c._codes = codes
#     # c._ordered = ordered
#     return c
#
# def _carray_to_series(c):
#     ind = pandas.Index(np.arange(c.shape[0]), dtype=int)
#     return pandas.Series(data=c, index=ind, fastpath=True)
