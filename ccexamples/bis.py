import commoncrawlscraper.lib as lib
import pandas as pd
url = 'http://www.bis.org/*'
r = lib.cc.search_all_crawls(url)
a = [x for x in r if '.pdf' in x['url']]
df = pd.DataFrame(a)
df = df.sort_values('timestamp')
d = df.groupby('url').last()
d = d.reset_index()
dr = d.to_dict(orient='records')
pdfs = list()
for x in dr:
    print(x['url'])
    res = lib.cc.get_crawl_from_json(x)
    pdfs.append(res)
