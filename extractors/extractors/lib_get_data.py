#!/usr/bin/env python
"""
Tools from uk land registry stuff. Mostly to do with curl and checking stuff.


So far no good way of hashing file at source. Just use length.
Can not wget directly to google bucket?
NOTES
gsutil hash gs:...
gsutil hash localfile
wget --spider url
gzip -l localfile
gunzip pp-2017.csv.gz -l
compressed uncompressed  ratio uncompressed_name
28876729    157279142  81.6% pp-2017.csv
"""
import subprocess
import zipfile
import gzip
import pandas as pd
import os
import inspect
import datetime
import argh
import tempfile
import json
import struct
from . import lib

_mydir = os.path.dirname(__file__)

try:
    _cache
except NameError as e:
    _cache = dict()


def whoami():
    frame = inspect.currentframe().f_back
    i = inspect.getframeinfo(frame)
    fname = os.path.basename(i.filename).replace('.py', '')
    fname = fname.replace('get_data_', '')  # more confusions
    # return os.path.join(fname, i.function)
    return i.function


def run_command_get_output(cmd, shell=True, splitlines=True):
    print('running {}'.format(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
    out, err = p.communicate()
    status = p.returncode
    out = out.decode()
    err = err.decode()
    if splitlines:
        out = out.split('\n')
        err = err.split('\n')
    return dict(out=out, err=err, status=status)


def getinfo_gzip(filename):
    # using last 4 bytes (not safe)
    d = dict()
    f = open(filename, 'rb')
    f.seek(-4, 2)
    d['uncompressed'] = struct.unpack('I', f.read(4))[0]
    return d


def getinfo_gzip_old(filename):
    cmd = 'gzip -l $(realpath {})'.format(filename)
    res = run_command_get_output(cmd, splitlines=False)
    a = res['out'].strip().split('\n')
    assert len(a) == 2, 'Expected length 2, got len {}: {} {}'.format(len(a), a, res)
    a = [x.strip().split() for x in a]  # len 2
    a = dict(zip(a[0], a[1]))
    return a


def is_gzip(filename):
    if filename.endswith('.gz') or '.gz.' in filename:
        return True
    return False


def is_zip(filename):
    if filename.endswith('.zip') or '.zip.' in filename:
        return True
    return False


def getinfo_zip(filename):
    # using last 4 bytes (not safe)
    b = zipfile.ZipFile(filename, 'r')
    x = b.infolist()
    # assert len(x) == 1, 'Got len > 1: {}'.format(x)
    # x = x[0]
    # x.filename
    # d = dict()
    d = list()
    for x in b.infolist():
        tmp = dict()
        for k in ['filename', 'compress_type', 'external_attr', 'file_size']:
            tmp[k] = getattr(x, k)
        d.append(tmp)
    if len(d) == 1:
        d = d[0]
    else:
        d = dict(multi=d, file_size=sum([x['file_size'] for x in d]))
    return d


def get_meta_data(filename):
    # might need to just check for .gzip. or .zip. due to dating convention
    d = dict()
    m = os.stat(filename)
    d['st_size'] = m.st_size
    d['st_mtime'] = m.st_mtime
    if is_zip(filename):
        tmp = getinfo_zip(filename)
        d.update(tmp)
        d['uncompressed'] = tmp['file_size']
        d['dirty_check'] = d['st_size']
    elif is_gzip(filename):
        tmp = getinfo_gzip(filename)
        d.update(tmp)
        d['dirty_check'] = d['uncompressed']
    return d


class StandardExtractor():
    """
    wget with spider check
    Use class as namespace to define a basic API
    Things with no arg just ignore the arg for now.
    """
    # this pattern is a bit weird, was from the uk stuff simplify later if needed
    _datadir_appendonly = os.path.join(lib._basedir, 'tmp/lib_get_data/data_appendonly/{name}')
    _datadir = os.path.join(lib._basedir, 'tmp/lib_get_data/data/{name}')
    _tempdir = os.path.join(lib._basedir, 'tmp/lib_get_data/tmp')

    def __init__(self, name, get_args, render_arg):
        self.name = name
        self.datadir_appendonly = self._datadir_appendonly.format(name=self.name)
        self.datadir = self._datadir.format(name=self.name)
        self._render_arg = render_arg
        for _dir in [self.datadir_appendonly, self._tempdir, self.datadir]:
            if not os.path.exists(_dir):
                os.makedirs(_dir)
        self.get_args = get_args

    def render_arg(self, arg):
        """
        stuff for a single check, get, write step ...
        return {'url': ..., 'filename': ..., 'arg': ...}
        """
        d = self._render_arg(arg)
        assert set(d.keys()) == {'url', 'filename', 'arg'}, 'must provide correct keys url filename arg'
        filename = d['filename']
        if is_gzip(filename) or is_zip(filename):
            d['dest'] = os.path.join(self.datadir_appendonly, '{}'.format(filename))
            d['link'] = os.path.join(self.datadir, filename)
        else:
            filenamegz = filename + '.gz'
            d['dest'] = os.path.join(self.datadir_appendonly, '{}'.format(filenamegz))
            d['link'] = os.path.join(self.datadir, filenamegz)
        d['meta'] = d['dest'] + '.meta'
        return d

    def source_stat(self, arg):
        global _cache
        key = (self.name, arg)
        if key in _cache:
            return _cache[key]
        d = self.render_arg(arg)
        url = d['url']
        cmd = 'wget --spider {}'.format(url)
        res = run_command_get_output(cmd)
        if any(['400 Bad Request' in x for x in res['err']]):
            raise Exception('ERROR ... probably site does not allow wget --spider checks or the url is bad. Just get_file since there is not fast way to check: {}'.format(res))
        a = [x for x in res['err'] if x.startswith('Length')]
        assert len(a) == 1, 'Expected length 1 got {}:{}'.format(len(a), a)
        a = a[0].split()
        a = a[1]
        final = dict()
        final['json'] = dict(length=a, rendered=d, status='ok')
        _cache[key] = final
        return final

    def _regen_meta_data(self, arg):
        d = self.render_arg(arg)
        # TODO need to follow  link
        d['link']
        pass
    def file_stat(self, arg):
        regen_meta_data = True  # for fixing/debug
        d = self.render_arg(arg)
        link = d['link']
        meta = d['meta']
        if not os.path.exists(link):
            return dict(status='missing', rendered=d)
        elif not os.path.exists(meta):
            if regen_meta_data:
                a = get_meta_data(link)
                print('writing {}'.format(meta))
                json.dump(a, open(meta, 'w'))
            else:
                raise Exception('meta not exist {}'.format(meta))
        meta_data = json.loads(open(meta).read())
        return dict(status='exists', rendered=d, json=meta_data)

    def check_local_dirty_clean(self, arg):
        a = self.file_stat(arg)
        b = self.source_stat(arg)
        dirty = True
        if a.get('status') == 'missing':
            dirty = True
        else:
            a_size = int(a['json']['dirty_check'])
            b_size = int(b['json']['length'])
            if a_size == b_size:
                dirty = False
        res = dict(file_stat=a, source_stat=b, dirty=dirty)
        return res

    def get_file(self, arg):
        d = self.render_arg(arg)
        temp = os.path.join(tempfile.mkdtemp(dir=self._tempdir), 'tmpfile')
        filename = d['filename']
        if is_zip(filename) or is_gzip(filename):
            filename_final = filename
            dest = os.path.join(self.datadir_appendonly, '{}.{}'.format(filename_final, datetime.datetime.today().isoformat()))
            cmd = 'wget -v {url} -O {temp} && mv {temp} {dest}'.format(url=d['url'], temp=temp, dest=dest)
        else:
            filename_final = filename + '.gz'
            dest = os.path.join(self.datadir_appendonly, '{}.{}'.format(filename_final, datetime.datetime.today().isoformat()))
            cmd = 'wget -v {url} -O {temp} && gzip {temp} && mv {temp}.gz {dest}'.format(url=d['url'], temp=temp, dest=dest)
        res = run_command_get_output(cmd)
        if res['status'] != 0:
            raise Exception(res)
        else:
            link = os.path.join(self.datadir, filename_final)
            if os.path.exists(link):
                os.remove(link)
            print("symlinking {} {} and writing meta data {}".format(dest, link, d['meta']))
            os.symlink(dest, link)
            meta_data = get_meta_data(dest)
            json.dump(meta_data, open(d['meta'], 'w'))
        return res

    def maybe_get_one(self, arg):
        res = self.check_local_dirty_clean(arg)
        if res['dirty']:
            print('{} is dirty. pulling data. {}'.format(arg, res))
            self.get_file(arg)
        else:
            print('{} is clean. not pulling data'.format(arg))

    def maybe_get_all(self):
        args = self.get_args()
        if args is None:
            self.maybe_get_one(args)
        else:
            for arg in self.get_args():
                self.maybe_get_one(arg)

    def get_parser(self, parser=None):
        if parser is None:
            parser = argh.ArghParser()
        # print('adding {}'.format(self.name))
        parser.add_commands([self.get_args, self.maybe_get_all, self.maybe_get_one, self.get_file, self.check_local_dirty_clean], namespace=self.name)
        return parser

    def dispatch(self):
        argh.dispatch_commands([self.get_args, self.maybe_get_all, self.maybe_get_one, self.get_file, self.check_local_dirty_clean])


def get_parser(*extractors):
    parser = argh.ArghParser()
    for e in extractors:
        # add using namespace
        parser = e.get_parser(parser=parser)
    return parser
