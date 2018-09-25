from .io_dict_of_things_and_carrays import *
def cachecalc(basepath=None):
    """ basic bundler and serializer of dict outputs. Tries to use **kwargs using default_namer (*args is banned). """

    def default_namer(fun, args, kwargs):
        """ try best attempt make a name """
        argspec = inspect.getfullargspec(fun)
        all_args = dict(zip(argspec.args, args))
        all_args.update(kwargs)
        return ['{}={}'.format(k, all_args[k]) for k in sorted(all_args.keys())]

    reg = re.compile('\.py$')
    def inner(fun):
        """ This one is not returned """
        # set the base basepath, really need to refactor to Class
        _basepath = basepath
        if _basepath is None:
            _basepath = 'things'
        _basepath = os.path.join(_basepath, '{}:{}'.format(reg.sub('', os.path.basename(inspect.getmodule(fun).__file__)), fun.__name__)) # basically use pwd
        if not os.path.exists(os.path.dirname(_basepath)):
            os.makedirs(os.path.dirname(_basepath))
        def _inner(fun, *args, **kwargs):
            """ this one is returned """
            _path = _basepath
            if type(_path) is str:
                tmp = '_'.join(default_namer(fun, args, kwargs))
                if tmp == '':
                    tmp = '__noargs__' # TODO is this the only place ... yikes
                tmp = '{}.things'.format(tmp) if tmp else '.things'
                # what about '/' in tmp ?
                _path = os.path.join(_path, tmp) # save locally, could get weird with this default
            if hasattr(_path, '__call__'):
                _path = _path(**kwargs) # in case you want to do something else?
            assert type(_path) is str
            print("checking cache {}".format(_path))
            if os.path.exists(_path) and not _inner._dirty:
                d = from_dict_of_things(_path)
            else:
                d = fun(*args, **kwargs)
                to_dict_of_things(d, _path)
                _inner._dirty = False
            return d
        _inner = decorator.decorate(fun, _inner)
        _inner._dirty = False
        def list_caches():
            """ list .things that have been computed """
            # if you need to parse the filenames, you need to rewrite this using a better args, kwargs storing mechanisi and a hash
            files = glob.glob('{}*.things'.format(_basepath))
            return files
        def load_all_caches():
            """ load .things that have been computed """
            files = glob.glob('{}*.things'.format(_basepath))
            return {k: from_dict_of_things(k) for k in files}
        def poison_cache():
            _inner._dirty = True
        def force_clean():
            _inner._dirty = False
        def is_dirty():
            return _inner._dirty
        _inner.poison_cache = poison_cache
        _inner.is_dirty = is_dirty
        _inner.force_clean = force_clean
        _inner.load_all_caches = load_all_caches
        _inner.list_caches = list_caches
        _inner.basepath = _basepath
        return _inner
    return inner

