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


