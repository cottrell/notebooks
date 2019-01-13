from . import lib
import pandas as pd
from .lib_get_data import StandardExtractor
_mydir, _myname = lib.say_my_name()

def get_all_price_paid():
    for x in get_args():
        get_price_paid(x)

def get_all_price_paid_by_county():
    for x in get_args():
        get_price_paid_by_county(x)

def _get_price_paid(year):
    pricepaid.maybe_get_one(year)
    filename = pricepaid.render_arg(year)['link']
    df = pd.read_csv(filename, compression='gzip', header=None, dtype=str)
    df.columns = ['id', 'price', 'date', 'postcode', 'property_type', 'old_new', 'duration', 'paon', 'saon', 'street', 'locality', 'town', 'district', 'county', 'ppdcategorytype', 'addchangedelete']
    schema = {'id': 'object',
              'price': 'int64',
              'date': 'object',
              'postcode': 'object',
              'property_type': 'object',
              'old_new': 'object',
              'duration': 'object',
              'paon': 'object',
              'saon': 'object',
              'street': 'object',
              'locality': 'object',
              'town': 'object',
              'district': 'object',
              'county': 'object',
              'ppdcategorytype': 'object',
              'addchangedelete': 'object'
              }
    lib.apply_schema_to_df_inplace(df, schema)
    return df

@lib.extractor(partition_cols=['year'])
def get_price_paid(year):
    df = _get_price_paid(year)
    yield {'year': year}, df

@lib.extractor(partition_cols=['county'])
def get_price_paid_by_county(year):
    df = _get_price_paid(year)
    yield {}, df

def render_arg(year):
    _url = 'http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com'
    url = '{}/pp-{}.csv'.format(_url, year)
    filename = 'pp-{}.csv'.format(year)
    return dict(url=url, filename=filename, arg=year)
get_args = lambda : range(1995, 2019)
pricepaid = StandardExtractor('pricepaid', get_args, render_arg)

