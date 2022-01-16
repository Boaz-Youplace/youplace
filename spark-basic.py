import json 

from pyspark.sql import SparkSession

spark = SparkSession\
        .builder\
        .appName('Python Spark SQL basic example')\
        .config('spark.some.config.option', 'some-value')\
        .getOrCreate()

### Create json file using spark
# sparkContext로 객체 생성
sc = spark.sparkContext

path = './json_files/test.json'
peopledf = spark.read.json(path)

peopledf.printSchema()
