from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, window
from pyspark.sql.functions import split
from pyspark.sql.types import *

spark = SparkSession.builder.appName("files").getOrCreate()

import pyspark.sql.types as t
schema = t.StructType([
    t.StructField("a", t.StringType()),
    t.StructField("d", t.DoubleType()),
    t.StructField("e", t.DoubleType()),
    t.StructField("b", t.DoubleType()),
    t.StructField("f", t.StringType()),
    t.StructField("c", t.DoubleType()),
    t.StructField("g", t.StringType())
    ])

df = spark.readStream.csv(schema=schema, path='data/*.csv.gz')

# Print new data to console
# d = df.writeStream.format("console").start()
# call d.stop to stop

# Write new data to Parquet files
df \
    .writeStream \
    .format("parquet") \
    .option("checkpointLocation", "checkpoints") \
    .option("path", "data.parquet/") \
    .start()

# # ========== DF with aggregation ==========
# aggDF = df.groupBy("device").count()
# 
# # Print updated aggregations to console
# aggDF \
#     .writeStream \
#     .outputMode("complete") \
#     .format("console") \
#     .start()
# 
# # Have all the aggregates in an in memory table. The query name will be the table name
# aggDF \
#     .writeStream \
#     .queryName("aggregates") \
#     .outputMode("complete") \
#     .format("memory") \
#     .start()
# 
# spark.sql("select * from aggregates").show()   # interactively query in-memory table
