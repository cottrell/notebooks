import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import QuantileTransformer

# NOTE: Make sure that the class is labeled 'target' in the data file
import competitions
d = competitions.get_data()
tpot_data = d.data
features = tpot_data.drop('target', axis=1).values
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'].values, random_state=None)

# Average CV score on the training set was:-798262.3003331326
exported_pipeline = make_pipeline(
    QuantileTransformer(),
    QuantileTransformer(),
    GaussianProcessRegressor(alpha=0.0001)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
train_results = exported_pipeline.predict(training_features)
from pylab import *
# figure(1)
# clf()
# ion()
# plot(training_target, train_results, 'bo')
# plot(testing_target, results, 'ro')
# show()

competitions.plot_predict(exported_pipeline)
