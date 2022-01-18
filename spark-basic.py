import json 

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf

spark = SparkSession\
        .builder\
        .appName('Python Spark SQL basic example')\
        .config('spark.some.config.option', 'some-value')\
        .getOrCreate()

# path 네임 [group_id]_[파티션0 기준 offset]으로 설정
path = './json_files/test.json'

# 데이터프레임 생성
df = spark.read.json(path)    
df.printSchema()

print("after")


extract_element = udf(lambda x: x[0])

df=df.withColumn('x', extract_element(df["x"]))
df=df.withColumn('y', extract_element(df["y"]))
df=df.withColumn('place_name', extract_element(df["place_name"]))

df.printSchema()

# 스파크 데이터프레임에 SQL을 적용시킬 수 있는 객체(for 통계처리) 별도 생성
df.createOrReplaceTempView("object_1")
spark.sql("DESCRIBE object_1").show()