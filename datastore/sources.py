import os
import numpy as np
import pandas as pd
import Quandl
token = os.environ['QUANDL_AUTH']
mydir = os.path.dirname(os.path.realpath(__file__))
basepath = os.path.join(mydir, 'data_cache')
from . import bc

@bc.cachecalc(basepath=basepath)
def _get_from_quandl(code=None, **kwargs):
    return {'data': Quandl.get(code, authtoken=token).reset_index()}

def _get_currencies():
    filename = os.path.join(mydir, 'major_currencies.tab')
    df_currfx = pd.read_csv(filename, sep='\t')
    currencies = df_currfx['Currency Code'].tolist()
    return currencies

class BlankObject():
    pass

class QuandlReader():
    def __init__(self):
        self._setup_currfx_readers()
    def _setup_currfx_readers(self):
        base_currency = 'USD'
        currencies = _get_currencies()
        database = 'CURRFX'
        codes = [os.path.join(database, '{}{}'.format(k, base_currency)) for k in currencies]
        obj = BlankObject()
        for code in codes:
            name = code.split('/')[1] # first part is database
            cache_key = os.path.join(basepath, code)
            def fun(code=code):
                return _get_from_quandl(code=code)['data'].set_index('Date')
            setattr(obj, name, fun)
        @bc.cachecalc(basepath=os.path.join(basepath, database, 'all'))
        def get_all():
            dfs = list()
            for code in codes:
                name = code.split('/')[1] # first part is database
                temp = getattr(obj, name)()
                temp.columns = ["{}_{}".format(name, x) for x in temp.columns]
                dfs.append(temp)
            dfs = pd.concat(dfs, axis=1)
            return {'data': dfs}
        obj.get_all = lambda : get_all()['data']
        def get_all_cleaned():
            df = obj.get_all()
            df = df[[x for x in df.columns if x.endswith('Rate')]]
            m = df.mean()
            s = df.std()
            z = (df - m).abs() / s
            df[z > 10] = np.nan
            return df
        obj.get_all_cleaned = get_all_cleaned
        setattr(self, database, obj)

quandl = QuandlReader()
