import json 

from pyspark.sql import SparkSession

spark = SparkSession\
        .builder\
        .appName('Python Spark SQL basic example')\
        .config('spark.some.config.option', 'some-value')\
        .getOrCreate()

# path 네임 [group_id]_[파티션0 기준 offset]으로 설정
test_path = './json_files/cars.json'
path = './json_files/test.json'

jeju_df = spark.read.json(path)
jeju_df.show(5)
jeju_df.printSchema()

test_df = spark.read.json(test_path)
test_df.show(5)
test_df.printSchema()

