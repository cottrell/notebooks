"""
want to get a rough idea of accidents:
    {cyclist, pedestrian, driver} killed
    {cyclist, pedestrian, driver} involved

    determined killed by '{} injured in' mapping
    determined involved by '... injured in ...' (collision with?)

"""
import bc
import pandas as pd
df = bc.from_carrays('DeathRecords.carrays')

import re
reg = re.compile(' of | with | in ')

d = df[df.MannerOfDeath == 'Accident']
d = d[d.Icd10Code.str.contains(' injured in ') & d.Icd10Code.str.contains(' traffic accident') & ~d.Icd10Code.str.contains(' construction vehicle')]
d = d[~d.Icd10Code.str.contains(' all-terrain')]
d = d[~d.Icd10Code.str.contains(' special agricultural vehicle')]
d = d[~d.Icd10Code.str.contains('Bus occupant')]

a = d.Icd10Code.astype(str).unique().tolist()
b = [x.split(':')[0] for x in a]

def _get_injured(x):
    x = x.lower()
    d = ['pedestrian', 'motorcycle', 'bus occupant', 'streetcar', 'cyclist']
    for k in d:
        if k in x:
            return k
    d = ['car occupant', 'occupant [any] of pick-up truck or van', 'occupant of pick-up truck or van', 'driver', 'passenger', 'car occupant [any]', 'occupant of three-wheeled motor vehicle', 'occupant of heavy transport vehicle', 'unspecified occupant of heavy transport vehicle', 'occupant [any] of heavy transport vehicle', 'unspecified car occupant', 'driver of special industrial vehicle', 'unspecified occupant of pick-up truck or van', 'unspecified occupant of special industrial vehicle']
    for k in d:
        if k in x:
            return 'auto'
    return 'unknown'


def get_features(x):
    x = x.lower()
    x = x.split(':')[0]
    x = x.split(' injured in ')
    # assert len(x) == 2, '{} not 2 length'.format(x)
    if len(x) == 1:
        x = x + ['None']
    return x

injured_map = {
 'bus occupant': 'bus occupant',
 'car occupant': 'auto',
 'car occupant [any]': 'auto',
 'driver': 'auto',
 'driver of special industrial vehicle': 'auto',
 'motorcycle rider': 'motorcycle',
 'motorcycle rider [any]': 'motorcycle',
 'occupant [any] of heavy transport vehicle': 'auto',
 'occupant [any] of pick-up truck or van': 'auto',
 'occupant of heavy transport vehicle': 'auto',
 'occupant of pick-up truck or van': 'auto',
 'occupant of streetcar': 'streetcar',
 'occupant of three-wheeled motor vehicle': 'auto',
 'passenger': 'auto',
 'pedal cyclist': 'cyclist',
 'pedal cyclist [any]': 'cyclist',
 'pedestrian': 'pedestrian',
 'unspecified car occupant': 'auto',
 'unspecified motorcycle rider': 'motorcycle',
 'unspecified occupant of heavy transport vehicle': 'auto',
 'unspecified occupant of pick-up truck or van': 'auto',
 'unspecified occupant of special industrial vehicle': 'auto',
 'unspecified pedal cyclist': 'cyclist'}

involving_map = {
 'traffic accident involving other and unspecified motor vehicles': 'auto',
 'noncollision transport accident': 'auto',
 'collision with car, pick-up truck or van': 'auto',
 'collision with heavy transport vehicle or bus': 'auto',
 'unspecified traffic accident': 'auto',
 'collision with other and unspecified motor vehicles in traffic accident': 'auto',
 'collision with two- or three-wheeled motor vehicle': 'auto',
 'collision with fixed or stationary object': 'None',
 'collision with railway train or railway vehicle': 'railway',
 'collision with pedestrian or animal': 'pedestrian',
 'collision with other nonmotor vehicle': 'nonauto',
 'collision with pedal cycle': 'cyclist',
 'collision with other pedal cycle': 'cyclist',
 'traffic accident': 'auto'}

# for figuring things out
# c = [get_features(x) for x in b]
# c = pd.DataFrame(c)
# c.index = a
# c['injured'] = c[0].map(_get_injured)
# c['involving'] = c[1].map(involving_map)

temp = d.Icd10Code.map(lambda x: get_features(x)[0])
d['injured'] = temp.map(injured_map)
temp = d.Icd10Code.map(lambda x: get_features(x)[1])
d['involving'] = temp.map(involving_map)
cols = ['injured', 'involving']
# cols = ['involving', 'injured']
for k in cols:
    d[k] = d[k].astype('category')

keep = ['auto', 'pedestrian', 'cycle', 'motorcycle']

a = d.groupby('injured').size()
a.sort()
print(a)
a = d.groupby('involving').size()
a.sort()
print(a)
a = d.groupby(cols).size()
a.sort()
a = a.sort_index()
print(a)

a = a.unstack().fillna(0)
# a.columns = a.columns.to_native_types() # categorical index does like me

c = a.copy()

cols = ['auto', 'cyclist', 'motorcycle', 'pedestrian', 'streetcar', 'railway']
aa = a.reindex_axis(cols, axis=0).fillna(0)
aa = aa.reindex_axis(['None', 'nonauto'] + cols, axis=1).fillna(0)
base = aa[['None', 'nonauto']].sum(axis=1)
aa = aa.drop(['None', 'nonauto'], axis=1)
base_self = pd.Series({k: aa.loc[k, k] for k in cols})
base_total = base + base_self
base_total.index.names = ['injured']

increase = dict()
for k in cols:
    for kk in cols:
        if k == kk:
            continue
        increase[(k, kk)] = aa.loc[k, kk] / float(1 + base_total[k])

increase = pd.Series(increase)
increase.index.names = ['injured', 'involving']

aa = pd.DataFrame(aa.stack())
aa.columns = ['incidents']
aa = aa.reset_index()
aa['base'] = aa.injured.map(base_total)
aa = aa.set_index(['injured', 'involving'])
aa['%increase_in_risk'] = aa['incidents'] / (1 + aa['base']) * 100
