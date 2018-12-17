#!/usr/bin/env python
import pandas as pd
import json
import pandas_datareader as pdr
import pandas_datareader.fred as fred
import functools
import os
from . import lib
_mydir, _myname = lib.say_my_name()

@lib.extractor()
def get_fred_meta_rate_daily():
    return fred.get_series_by_tag('rate;daily')

def _get_yahoo_product_map():
    d = json.load(open(os.path.join(_mydir, 'yahoo_meta.json')))
    dd = dict()
    for k in d:
        for kk in d[k]:
            if kk in dd:
                raise Exception('name collision between ticker {}'.format(kk))
            dd[kk] = k
    return dd

_yahoo_product_map = _get_yahoo_product_map()

def _get_yahoo_args():
    kwargs = {}
    for symbol, product in _yahoo_product_map:
        args = (symbol,)
        yield args, kwargs

def _yahoo_filename(symbol):
    product = _yahoo_product_map[symbol]
    return 'product={}/symbol={}'.format(product, symbol)

# 2000 per hour max
@lib.extractor(
arg_generator=_get_yahoo_args,
filename_generator=_yahoo_filename,
)
def get_yahoo_price_volume(symbol, start=None, end=None):
    start, end = lib.render_date_arg(start, end)
    # pdr should have a rate limit in my hacked version
    # need to fix scheme/enforce etfs/stocks different
    return pdr.DataReader(symbol, data_source='yahoo', start=start, end=end).reset_index()
