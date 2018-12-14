import inspect
import os
import sys

def say_my_name():
    depth = -1
    frame = sys._getframe(depth)
    _locals = frame.f_back.f_locals
    filename = os.path.realpath(_locals['__file__'])
    myname =  os.path.basename(filename).replace('.py', '')
    mydir = os.path.dirname(filename)
    if myname == '__init__':
        myname = os.path.basename(mydir)
    assert '_extractor' in myname
    myname = myname.replace('_extractor', '')
    basedir = get_basedir(myname)
    datadir = os.path.join(basedir, 'data')
    metadatadir = os.path.join(basedir, 'metadata')
    # TODO: consider named tuple
    dirs = [mkdir_if_needed(x) for x in [mydir, myname, basedir, datadir, metadatadir]]
    return dirs

def get_basedir(extractor_name):
    return os.path.join(os.path.expanduser('~/projects/data/extractor={}'.format(extractor_name)))

def mkdir_if_needed(k):
    if not os.path.exists(k):
        print('mkdir {}'.format(k))
        os.makedirs(k)
    return k
