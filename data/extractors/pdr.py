#!/usr/bin/env python
"""
"""
import pandas as pd
import pandas_datareader as pdr
import pandas_datareader.fred as fred
import functools
import os
from . import lib
# _mydir, _myname, _basedir, _datadir, _metadatadir = lib.say_my_name()

@lib.extractor()
def get_fred_meta_rate_daily():
    return fred.get_series_by_tag('rate;daily')

# def get_sources():
#     sources_filename = os.path.join(_mydir, 'sources.csv')
#     return pd.read_csv(sources_filename)
# 
# def get_data(name, symbol, start, end):
#     pdr.DataReader(symbol, data_source=name, start=start, end=end)
