from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, window
from pyspark.sql.functions import split

# run in another process: nc -lk 9999
# or dataserver.sh

spark = SparkSession \
    .builder \
    .appName("StructuredNetworkWordCount") \
    .getOrCreate()

# Create DataFrame representing the stream of input lines from connection to localhost:9999
lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# Split the lines into words
words = lines.select(
   explode(
       split(lines.value, " ")
   ).alias("word")
)

# Generate running word count
wordCounts = words.groupBy("word").count()

output_mode = "complete"
# output_mode = "append"

# Start running the query that prints the running counts to the console
query = wordCounts \
    .writeStream \
    .outputMode(output_mode) \
    .format("console") \
    .start()

query.awaitTermination()
