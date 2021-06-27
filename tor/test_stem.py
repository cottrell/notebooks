#!/usr/bin/env python
import requests
from stem import Signal
from stem.control import Controller

proxies = {'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}

with Controller.from_port(port=9051) as c:
    c.authenticate()
    c.signal(Signal.NEWNYM)

print(requests.get('https://api.ipify.org', proxies=proxies).text)
from fake_useragent import UserAgent

headers = {'User-Agent': UserAgent().random}
res = requests.get('https://api.ipify.org', proxies=proxies, headers=headers)
print(res)
print(res.text)
