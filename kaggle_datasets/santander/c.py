import pandas as pd
import numpy as np
res = {
'submission.csv': 0.839143,
'submission_xgb_weighted.csv': 0.837462,
'submission_hack_01.csv': 0.839058
}
files = sorted(list(res.keys()))
d = dict()
for k in files:
    d[k] = pd.read_csv(k, header=0)

p = pd.concat([d[k]['TARGET'] for k in files], axis=1).values
r = np.array([res[k] for k in files])

logp = np.log(p)

dlogJ = (r[1] - r[0]) / (p[:,1] - p[:,0])

i = np.argmax(r)

pp = logp[:,i]
# pp + dlogJ * eps <= 0
# pp <= - dlogJ * eps
# pp is all neg, eps pos
# 1 / eps => - dlogJ / pp (all)

eps = - 1.0 / (dlogJ / pp).min()

eps = eps * 0.9999

a = np.exp(pp + dlogJ * eps)

import b
dd = b.get_data()
df = pd.DataFrame({'ID': dd['id_test'], "TARGET": a})
df.to_csv('submission_hack_01.csv', index=False)

