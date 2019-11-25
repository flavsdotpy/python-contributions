# Requires:
#
# pyspark



# The addidional needed packages are added with this configuration.
# The packages MUST follow this structure >> groupId:artifactName:version
# For more than one package, separate them with commas. (Just like in the example)


from pyspark.sql import SparkSession

spark = SparkSession.builder.master('local[*]')\
    .config("spark.jars.packages", "com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.3")\
    .getOrCreate()