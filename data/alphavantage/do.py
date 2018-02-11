from alpha_vantage.timeseries import TimeSeries
import os
import json
apikey = json.load(open(os.path.expanduser('~/.cred/alphavantage/auth.json')))['APIKEY']
ts = TimeSeries(key=apikey, output_format='pandas')
# Get json object with the intraday data and another with  the call's metadata
# data, meta_data = ts.get_intraday('GOOGL')
# print(meta_data)
# print(data)
