"""
fetch("https://api.tradingeconomics.com/calendar", {"credentials":"include","headers":{"accept":"application/json, text/javascript, */*; q=0.01","accept-language":"en-US,en;q=0.9"},"referrer":"https://tradingeconomics.com/calendar","referrerPolicy":"no-referrer-when-downgrade","body":null,"method":"GET","mode":"cors"});
fetch("https://tradingeconomics.com/calendar", {"credentials":"include","headers":{"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","accept-language":"en-US,en;q=0.9","cache-control":"max-age=0","upgrade-insecure-requests":"1"},"referrer":"https://tradingeconomics.com/calendar","referrerPolicy":"no-referrer-when-downgrade","body":null,"method":"GET","mode":"cors"});
"""
import argh
import numpy as np
import gzip
import pandas as pd
import tqdm
import dateutil
import datetime
import re
from lxml import html, etree
# filename = "Economic Calendar_2015010_20150922.html.gz"

def parse_file(filename):
    text = gzip.open(filename).read()
    tree = html.fromstring(text)

    def get_row(e):
        row = list()
        for x in e.iterchildren():
            row.append(reg.sub(' ', x.text_content().strip()))
        return row

    table = tree.xpath('//table[@id="calendar"]')
    assert len(table) == 1
    table = table[0]
    tr = table.xpath('./*/tr')

    # matches things like 'Thursday January 01 2015'
    reg_is_not_header = re.compile('.*(AM|PM)$')

    df = list()
    def is_header(x):
        if reg_is_not_header.match(x):
            return False
        return True

    header = ['Actual', 'Previous', 'Consensus', 'Forecast', ''] # last one not used?
    date = None
    for i, x in tqdm.tqdm(enumerate(tr)):
        row = get_row(x)
        if is_header(row[0]):
            date = row[0]
            assert row[1:] == header, '{} != {}. First entry is {}'.format(row[1:], header, row[0])
            continue
        row.insert(0, date)
        df.append(row)

    df = pd.DataFrame(df, columns = ['Date', 'Time', 'Country', 'Name'] + header)
    df.columns = [x.lower() for x in df.columns]
    df['date'] = pd.to_datetime(df.date + ' ' + df.time)
    df = df.drop('time', axis=1)

    _factor = dict(zip(list('KMBT%'), [1e3, 1e6, 1e9, 1e12, 1]))

    def handle_number(x):
        x = x.replace(',', '')
        r = re.findall('^([^+-\.0-9]*)([+-\.0-9]*)([^+-\.0-9]*)', x)
        assert len(r) == 1
        pre, value, post = r[0]
        return pre.strip(), value.strip(), post.strip()

    def handle_number_column(df, colname):
        d = pd.DataFrame(df.actual.map(handle_number).values.tolist())
        d.columns = ['pre', 'value', 'post']
        d['value'] = d['value'].replace('', np.nan)

        # some bad data point. numbers look bad too.
        #                     date country                  name    actual previous consensus   forecast
        # 1936 2015-02-26 14:00:00      MX  Balance of Trade JAN  $-3248BM    $254M  $ -3151M  $ -527.7M
        d['post'] = d['post'].replace('BM', 'M')


        d['value'] = d['value'].astype(float) * d.post.map(_factor).fillna(1)
        d['unit'] = np.where(d['post'].isin(_factor), '', d['post'])
        check = ((d.unit != '') & (d.pre != ''))
        assert check.sum() == 0
        d['unit'] = np.where(d.pre != '', d.pre.values, d.post.values)
        d = d[['value', 'unit']]
        d.columns = ['{}_{}'.format(colname, k) for k in d.columns]
        df = pd.concat([df, d], axis=1)
        return df

    for k in ['actual', 'previous', 'consensus', 'forecast']:
        df = handle_number_column(df, k)

    return df

def parse_filenames(*filenames):
    dfs = list()
    for f in filenames:
        dfs.append(parse_file(f))
    df = pd.concat(dfs)
    return df

# print('writing out.parquet')
# df.to_parquet('out.parquet')
