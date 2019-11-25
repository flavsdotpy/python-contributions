from pyspark.context import SparkContext
from pyspark.sql import SparkSession


#SPARK CONTEXTS
sc = SparkContext()
spark = SparkSession.builder.appName('Example').getOrCreate()
spark.stop()

