import datetime
import pandas as pd
import json
import os

info = json.load(open(os.path.expanduser('~/.cred/personal_information/info.json')))

bday = datetime.datetime.strptime(info['david']['birthday'], "%Y-%m-%d").date()
begin  = datetime.date(datetime.date.today().year, 1, 1)
end = bday + datetime.timedelta(days=100 * 365)
dates = pd.date_range(begin, end)
df = pd.DataFrame(dates, columns=['date'])
for k in ['year', 'week', 'month', 'day', 'dayofyear', 'dayofweek', 'weekday_name']:
    df[k] = getattr(df.date.dt, k)

d = df.set_index(['year', 'month', 'day'])['dayofyear'].unstack('year').T

# TODO life tables to heatmap
