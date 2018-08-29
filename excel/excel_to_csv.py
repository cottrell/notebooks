#!/usr/bin/env python
import string
import argh
import os
import pandas as pd

def format_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_')
    return filename

_mydir = os.path.realpath(os.path.dirname(__file__))
_default_dir = os.path.join(_mydir, os.path.basename(__file__).rsplit('.', 1)[0])

def mangle_df(df):
    for k in df:
        df[k] = df[k].str.strip()
    return df

def _run(filename, outputdir=None):
    if outputdir is None:
        outputdir = _default_dir
    xl = pd.ExcelFile(filename)
    if len(xl.sheet_names) == 0:
        print("no sheets in {}".format(filename))
        return
    elif len(xl.sheet_names) > 1:
        outputdir = os.path.join(outputdir, os.path.basename(filename).rsplit('.', 1)[0])
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    for s in xl.sheet_names:
        print(s)
        df = xl.parse(s, dtype=str)
        print(s, df.shape)
        filename = os.path.join(outputdir, format_filename(s)) + '.csv'
        df = mangle_df(df)
        print(s, df.shape, filename)
        df.to_csv(filename, index=False)

def run(*filenames, outputdir=None):
    for filename in filenames:
        _run(filename)

if __name__ == '__main__':
    argh.dispatch_command(run)
