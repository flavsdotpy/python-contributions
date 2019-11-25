# Requires:
#
# pyspark

from pyspark.sql import SparkSession

spark = SparkSession.builder.master('local[*]').getOrCreate()


df = spark.read\
        .option('header', 'true').option('multiLine', 'true')\
        .option("ignoreTrailingWhiteSpace", 'true').option('inferSchema', 'true')\
        .csv('./sample.csv')