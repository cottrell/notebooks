fin = open('key.txt')
d = fin.readlines()
d = [x.strip() for x in d if x.strip()]
d = [x for x in d if not x.startswith('#')]
d = [x for x in d if not x.endswith('?')]
# d = [x.split(':')[0] for x in d]

def f(x):
    if ':' in x:
        x = x.split(':')[0] + ':'
    if '=' in x:
        x = [xx.strip() for xx in x.split('=')]
        assert len(x)==2
        try:
            int(x[0])
        except ValueError:
            int(x[1])
            x = [x[1], x[0]]
        x = '='.join(x)
    return x

d = [f(x) for x in d]

out = dict()
k = None
temp = dict()
for x in d:
    if ':' in x:
        if k is not None:
            out[k] = temp
            temp = dict()
        k = x.split(':')[0]
    if '=' in x:
        xx = x.split('=')
        temp[xx[0]] = xx[1]

dd = {k.replace(' ', '_'): {int(kk): vv for kk, vv in v.items()} for k, v in out.items()}
import json
json.dump(dd, open('key.json', 'w'))
