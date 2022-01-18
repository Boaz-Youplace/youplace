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

# 스파크 데이터프레임에 SQL을 적용시킬 수 있는 객체 별도 생성
jeju_df.createOrReplaceTempView("object_1")
spark.sql("SELECT * FROM object_1 LIMIT 3").show()
spark.sql("DESCRIBE object_1").show()