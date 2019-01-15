from lxml import html, etree
import numpy as np
import dateutil
import pandas as pd
from ratelimit import limits, sleep_and_retry
import os
import requests
from joblib import Memory
from . import lib
_mydir, _myname = lib.say_my_name()
cachedir = os.path.join(_mydir, 'joblib_cache')
memory = Memory(cachedir, verbose=10)

# # this does not work
# _unsold_url = 'http://www.auction.co.uk/residential/pastAuctions.asp?T=U'
# _past_results_url = 'http://www.auction.co.uk/residential/pastAuctions.asp?T=R'

# http://www.auction.co.uk/residential/pastresults.asp?A=1064&S=L&O=A&P=3
_min_n = 715 # dunno, this is where they seem to start, there are gaps, not sure.
_max_n = 1065
_url = 'http://www.auction.co.uk/residential/pastresults.asp?A={auction_number}&S=L&O=A&P={page}' # starts at 1

def get_all_data():
    # REMEMBER to clear the cache if you want to reforce it. This is the memory cache NOT the extractor data!
    # do everything at once, not too carefully since the memory.cache is being used anyway on each request
    for i in range(_min_n, _max_n+1):
        tmp = get_pastresults(i)

_period_seconds = 1
@memory.cache
@sleep_and_retry
@limits(calls=1, period=_period_seconds)
def make_request(url):
    r = requests.get(url)
    # Minimise the amount returned to reduce overheads:
    if r.status_code != 200:
        raise Exception('{} {}'.format(r.status_code, r.content))
    return r.content, r.status_code

_not_working = list()
_empty = list()

_manual = {
        'Lot 212 - £85,000 & Lot 213 - £15,000': (100000, 'Sold'),
        'Lots 48&49  £230,000 Collectively': (230000, 'Sold')
        }
def _handle_result(x):
    price_patterns = ('£', 'â\x82¬')
    if x in _manual:
        price, result = _manual[x]
        return price, result
    if x is None:
        return np.nan, None
    for k in price_patterns:
        if k in x:
            r = x.split(k)
            assert len(r) == 2
            #
            price = r[1].replace(k, '').replace(',', '').replace('+', '')
            if price.lower().endswith('m'):
                price = float(price[:-1]) * 1e6
            else:
                price = float(price)
            if 'available' in r[0].lower() or 'avaliable' in r[0].lower() or 'collectiv' in r[0].lower():
                result = 'Available'
            elif r[0] == '':
                result = 'Sold'
            else:
                raise Exception('something else with {}'.format(x))
            return price, result
    return np.nan, x


@lib.extractor()
def get_pastresults(auction_number):
    global _not_working, _empty
    pages = get_all_pages(auction_number)
    df = list()
    old_date = None
    for content, status, table, auction_date in pages:
        if old_date is not None:
            assert old_date == auction_date, 'got date mismatch unexpected {} {}'.format(old_date, auction_date)
        old_date = auction_date
        df.append(table)
    df = pd.concat(df)
    if df.shape[0] == 0:
        print('skipping auction_number {}. Appears empty'.format(auction_number))
        _empty.append(auction_number)
        raise StopIteration
    if "(NOT WORKING)" in auction_date:
        print('skipping auction_number {}. is labeled "NOT WORKING"'.format(auction_number))
        _not_working.append(auction_number)
        raise StopIteration
    df['auction_number'] = auction_number
    df['auction_date_string'] = auction_date
    if '&' in auction_date:
        auction_date = auction_date.split('&')[-1]
    df['auction_date'] = dateutil.parser.parse(auction_date)
    # try to enrich a bit
    s = df.result.apply(_handle_result).values
    x, y = list(zip(*s))
    df['price'] = x
    df['outcome'] = y
    yield {}, df

def get_all_pages(auction_number):
    pages = list()
    for i in range(10):
        url = _url.format(auction_number=auction_number, page=i+1)
        print(url)
        content, status = make_request(url)
        # the page changes each time, best to check the data. could use the "Lots" text but that is another dep
        tree = html.fromstring(content)
        auction_date = get_auction_date_from_tree(tree)
        table = get_table_from_tree(tree)
        if table.shape[0]:
            print('got empty table on auction_number {} page {}. breaking'.format(auction_number, i))
        if pages:
            last_table = pages[-1][2]
            if table.equals(last_table):
                print('current page same as last page, stopping at page {}'.format(i+1))
                break
        pages.append((content, status, table, auction_date))
    return pages

def get_auction_date_from_tree(tree):
    e = tree.xpath('//descendant-or-self::table[@class="Pagehead" and @id="Table10"]/tbody/tr/td')
    assert e[0].text.strip() == 'Past Auctions Results'
    assert len(e) == 2
    d = e[1].text.strip()
    d = ' '.join(d.split()[:-1])
    return d

def get_table_from_tree(tree):
    d = tree.xpath('//descendant-or-self::table[@class="Main"]/tr')
    table = list()
    for i, x in enumerate(d[1:]):
        td = x.xpath('./td') # a row?
        e = td[0]
        href = e.xpath('./a')[0].attrib['href']
        town = e.xpath('./a/span/span/span[@class="town"]')[0].text
        address = str(''.join(e.xpath('./a/span/span/span/following-sibling::text()'))).strip()
        location = str(td[2].xpath('./a')[0].text).strip()
        type_ = td[1].text
        result = td[3].text
        dd = {'type': type_, 'location': location, 'town': town, 'address': address, 'result': result, 'href': href}
        table.append(dd)
    df = pd.DataFrame(table)
    return df




# content, status = make_request(_past_results_url)
# tree = html.fromstring(content)
