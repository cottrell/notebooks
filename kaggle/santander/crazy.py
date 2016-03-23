from dataprep import *
import bc
df_train = d['train']
df_test = d['test']

def extreme_stacked_format():
    d = df_train[xcols].stack()
    d = d[d!=0]
    y = df_train[[ycol]].stack()
    d = pd.concat([d, y])
    del y
    d = d.reset_index()
    d.columns = ['ID', 'col', 'value']
    d = d.sort_values(by=['ID', 'col'])
    for k in ['ID', 'col']:
        d[k] = d[k].astype('category')
    return d

def get_data():
    try:
        d = bc.from_carrays('extreme_stacked.bcolz')
        print("read from extreme_stacked.bcolz")
    except Exception as e:
        print('re-processing from original data')
        d = extreme_stacked_format()
        bc.to_carrays(d, 'extreme_stacked_format.bcolz')
    return d
