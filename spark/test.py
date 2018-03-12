import socket
import os

import pyspark
sc = pyspark.SparkContext.getOrCreate()
def f():
    return os.environ['PYTHONPATH'], os.environ.get('SPARK_CONF_DIR', 'asdf'), os.environ.get('THIS', 'nope'), pyspark.TaskContext().stageId()

res = sc.parallelize(range(10)).map(lambda x: f()).distinct().collect()

print(sc.getConf().getAll())

print("")
print("")
print("")
print("")
for x in res:
    print(x)
print("")
print("")
print("")
print("")
