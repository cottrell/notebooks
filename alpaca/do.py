import alpaca_trade_api as tradeapi

import json
import os

name = 'alpaca'
cred = json.load(open(os.path.expanduser(f"~/.cred/{name}/cred.json")))


api = tradeapi.REST('<key_id>', '<secret_key>', api_version='v2') # or use ENV Vars shown below
account = api.get_account()
api.list_positions()
