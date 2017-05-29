"""
"""
import glob
import os
import datetime

def globs_with_timestamps(*patterns):
    out = list()
    for pattern in patterns:
        files = glob.glob(pattern)
        files = [(x, datetime.datetime.fromtimestamp(os.path.getmtime(x))) for x in files]
        out.extend(files)
    return out

import simplekv
import simplekv.fs
dbname = 'here.db'
store = simplekv.fs.FilesystemStore(dbname)

class GlobberRunner():
    def __init__(self, name, gen_patterns, version=None):
        self.name = name # TODO use inspect get from code
        self.gen_patterns = gen_patterns
        self.version = str(version) if version is not None else '0'
    def run_once(self, *args, **kwargs):
        patterns = self.gen_patterns(*args, **kwargs)
        if type(patterns) in {str, bytes}:
            patterns = [patterns]
        filenames_with_timestamps = globs_with_timestamps(*patterns)
        for x in filenames_with_timestamps:
            key = hash((self.name, self.version, x))
            value = (self.name, self.version, x)
            print(key, value)

g = GlobberRunner('test', lambda : 'data/*.csv.gz')
