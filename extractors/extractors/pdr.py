#!/usr/bin/env python
import time
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
    yield {}, fred.get_series_by_tag('rate;daily')

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

# 2000 per hour max, my version of pandas DataReader is throttled but count is not persisted

_maybe_inactive = dict()
def get_all_yahoo_equities_etfs(period='oneweek'):
    """ use period None for full history """
    _get_all_yahoo('equities/etfs', period=period)
def get_all_yahoo_fx(period='oneweek'):
    """ use period None for full history """
    _get_all_yahoo('fx', period=period)

def _get_all_yahoo(product, period='oneweek'):
    """ use period None for full history """
    global _maybe_inactive
    kwargs = {}
    start, end = lib.render_date_arg(period)
    if product == 'equities/etfs':
        for symbol in _yahoo_product_map:
            try:
                get_yahoo_price_volume(symbol, start=start, end=end)
            except (KeyError, pdr.base.RemoteDataError) as e:
                _maybe_inactive[symbol] = str(e)
        json.dump(_maybe_inactive, open('yahoo_errors_equities_etfs.json', 'w'))
    elif product == 'fx':
        bad_fx = dict()
        for x in _usd_pairs:
            try:
                get_yahoo_fx(x, start=start, end=end)
            except Exception as e:
                print('skipping {}: {}'.format(x, e))
                bad_fx[x] = str(e)
        json.dump(bad_fx, open('yahoo_errors_fx.json', 'w'))
    else:
        raise Exception('bad product: {}'.format(product))


_usd_pairs = ['EURUSD', 'JPYUSD', 'GBPUSD', 'CHFUSD', 'AUDUSD', 'NZDUSD', 'CADUSD', 'SEKUSD', 'NOKUSD', 'CZKUSD', 'EGPUSD', 'HUFUSD', 'ISKUSD', 'ILSUSD', 'PLNUSD', 'RONUSD', 'RUBUSD', 'ZARUSD', 'TRYUSD', 'UAHUSD', 'KWDUSD', 'SARUSD', 'AEDUSD', 'BHDUSD', 'OMRUSD', 'QARUSD', 'CNYUSD', 'HKDUSD', 'INRUSD', 'IDRUSD', 'KZTUSD', 'KRWUSD', 'MYRUSD', 'PHPUSD', 'SGDUSD', 'TWDUSD', 'THBUSD', 'VNDUSD', 'ARSUSD', 'BRLUSD', 'CLPUSD', 'COPUSD', 'MXNUSD', 'PENUSD']

@lib.extractor(partition_cols=['product', 'symbol'])
def get_yahoo_price_volume(symbol, start=None, end=None):
    product = _yahoo_product_map[symbol]
    start, end = lib.render_date_arg(start, end)
    # pdr should have a rate limit in my hacked version
    # need to fix scheme/enforce etfs/stocks different
    schema = {'Date': 'datetime64[ns]',
            'High': 'float64',
            'Low': 'float64',
            'Open': 'float64',
            'Close': 'float64',
            'Volume': 'float64',
            'Adj Close': 'float64',
            'ingress_time': 'datetime64[ns]'
            }
    # not sure about get_actions if we really need them
    df = pdr.DataReader(symbol, data_source='yahoo', start=start, end=end).reset_index()
    lib.apply_schema_to_df_inplace(df, schema)
    yield {'product': product, 'symbol': symbol}, df

@lib.extractor(partition_cols=['symbol'])
def get_yahoo_fx(symbol, start=None, end=None):
    start, end = lib.render_date_arg(start, end)
    # pdr should have a rate limit in my hacked version
    # need to fix scheme/enforce etfs/stocks different
    schema = {'Date': 'datetime64[ns]',
            'High': 'float64',
            'Low': 'float64',
            'Open': 'float64',
            'Close': 'float64',
            'ingress_time': 'datetime64[ns]'
            }
    df = pdr.yahoo.fx.YahooFXReader(symbol, start=start, end=end).read().reset_index()
    lib.apply_schema_to_df_inplace(df, schema)
    yield {'symbol': symbol}, df

# def fix():
#     schema = {'Date': 'datetime64[ns]',
#             'High': 'float64',
#             'Low': 'float64',
#             'Open': 'float64',
#             'Close': 'float64',
#             'Volume': 'float64',
#             'Adj Close': 'float64',
#             'ingress_time': 'datetime64[ns]'
#             }
#     for k in _get_yahoo_args():
#         filename = get_yahoo_price_volume.filename(*k[0], **k[1])
#         if os.path.exists(filename):
#             df = get_yahoo_price_volume.load(*k[0], **k[1])
#             if df.dtypes.to_dict() != schema:
#                 print('bad {}'.format(filename))
#                 os.system('rm -rf {}'.format(filename))


if __name__ == '__main__':
    get_all_yahoo_fx()
    get_all_yahoo_equities_etfs()
