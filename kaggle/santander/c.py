import pandas as pd
res = {
'submission.csv': 0.839143,
'submission_xgb_weighted.csv': 0.837462
}
files = ['submission.csv', 'submission_xgb_weighted.csv']
d = dict()
for k in files:
    d[k] = pd.read_csv(k, header=0)
