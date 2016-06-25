import os
import pandas as pd
import Quandl
token = os.environ['QUANDL_AUTH']
mydir = os.path.dirname(os.path.realpath(__file__))
basepath = os.path.join(mydir, 'data_cache')
import bc

class QuandlReader():
    """ with scrappy caching """
    def __init__(self, base_currency='USD'):
        self._base_currency = base_currency
        self._setup_currfx()
    def _setup_currfx(self):
        filename = os.path.join(mydir, 'major_currencies.tab')
        self._df_currfx = pd.read_csv(filename, sep='\t')
        self._currencies = self._df_currfx['Currency Code'].tolist()
        database = 'CURRFX'
        codes = [os.path.join(database, '{}{}'.format(k, self._base_currency)) for k in self._currencies]
        obj = get_sub_reader(codes)()
        setattr(self, database, obj)

def get_sub_reader(codes):
    database = codes[0].split('/')[0]
    class QuandlSubReader():
        def __init__(self):
            self.database = database
        @classmethod
        @bc.cachecalc(basepath=basepath)
        def _get(self, code=None, **kwargs):
            return {'data': Quandl.get(code, authtoken=token).reset_index()}
        # @bc.cachecalc(basepath=basepath) # does not handle multicolumn
        def _all(self, database=database):
            df = dict()
            for code in codes:
                name = code.split('/')[1] # first part is database
                df[name] = getattr(self, name).T
            df = pd.Panel.from_dict(df)
            df = df.transpose(2, 0, 1).to_frame().T
            return {'data': df}
        def get_all(self):
            return self._all()['data']
    for code in codes:
        name = code.split('/')[1] # first part is database
        setattr(QuandlSubReader, name, property(lambda self: self._get(code=code)['data'].set_index('Date')))
    return QuandlSubReader

quandl = QuandlReader()
