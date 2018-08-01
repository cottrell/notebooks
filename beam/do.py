import apache_beam as beam
import apache_beam.io as io
from apache_beam.options.pipeline_options import PipelineOptions
import glob
import os
import time

_mydir = os.path.dirname(os.path.realpath(__file__))

def pollwatch():
    seen = set()
    pattern = os.path.join(_mydir, 'data/*.csv.gz')
    while True:
        res = glob.glob(pattern)
        unseen = sorted(list(set(res) - seen))
        for x in unseen:
            yield x
        seen.update(unseen)
        time.sleep(1)

def f(x):
    print(x)
    return 'nothing'

with beam.Pipeline(options=PipelineOptions()) as p:
    # lines = p | beam.Create([1, 2, 3, 4]) | beam.ParDo(f)
    lines = p | beam.Create(pollwatch()) | beam.ParDo(f)
