#!/usr/bin/env python

import requests

url = 'https://ident.me'

without_tor = requests.get(url)

proxies = {'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}

with_tor = requests.get(url, proxies=proxies)

print(f'without tor {without_tor.text}')
print(f'with tor {with_tor.text}')
