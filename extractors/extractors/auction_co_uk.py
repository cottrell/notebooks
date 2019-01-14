from lxml import html, etree
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
_max_n = 1065
_url = 'http://www.auction.co.uk/residential/pastresults.asp?A={auction_number}&S=L&O=A&P={page}'

@lib.extractor()
def get_all_data():
    # REMEMBER to clear the cache if you want to reforce it. This is the memory cache NOT the extractor data!
    # do everything at once, not too carefully since the memory.cache is being used anyway on each request
    df = list()
    for i in range(_max_n):
        tmp = get_data_from_auction(i)
        df.append(tmp)
    df = pd.concat(df)
    return {}, df

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

def get_data_from_auction(auction_number):
    pages = get_all_pages(auction_number)
    df = list()
    date = None
    for content, status in pages:
        tree = html.fromstring(content)
        new_date = get_auction_date_from_tree(tree)
        if date is not None:
            assert date == new_date, 'got date mismatch unexpected {} {}'.format(date, new_date)
        date = new_date
        tmp = get_table_from_tree(tree)
        df.append(tmp)
    df = pd.concat(df)
    df['date'] = date
    return df

def get_all_pages(auction_number):
    pages = list()
    for i in range(10):
        try:
            url = _url.format(auction_number=auction_number, page=i)
            pages.append(make_request(url))
        except Exception as e:
            if i == 0:
                raise Exception('probably on first page! {}'.format(e))
            print('page {} error to max hit'.format(i))
            break
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
