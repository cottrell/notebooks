import glob
import json
import pandas as pd
import pytz
from datetime import datetime, timedelta
epoch = datetime(1970, 1, 1, tzinfo=pytz.UTC)

def convert_timestamp_usec_to_datetime(x):
    # TODO find real epoch
    return epoch + timedelta(microseconds=int(x))

def read_search_data():
    search_files = glob.glob('./searches/Takeout/Searches/*.json')
    d = list()
    for filename in search_files:
        print('reading {}'.format(filename))
        temp = json.load(open(filename))
        d.extend(temp['event'])
    print('read {} records'.format(len(d)))
    d = [x['query'] for x in d]
    # just take first timestamp
    d = [[x['id'][0]['timestamp_usec'], x['query_text']] for x in d]
    d = [(convert_timestamp_usec_to_datetime(x), y) for x, y in d]
    d = pd.DataFrame(d)
    d.columns = ['datetime', 'query']
    d['date'] = d.datetime.apply(lambda x: x.date())
    for k in ['day', 'hour', 'month', 'dayofweek', 'dayofyear', 'week']:
        d[k] = d.datetime.apply(lambda x: getattr(x, k))
    return d

def get_all_words(queries):
    out = list()
    for x in queries:
        x = x.split()

from pylab import *

def doplots(d):
    ion()
    for i, k in enumerate(['date', 'day', 'hour', 'month', 'dayofweek', 'dayofyear', 'week']):
        print(k)
        figure(i)
        ax = gca()
        d.groupby(k).size().plot(kind='bar', ax=ax)
        ax.set_title(k)

