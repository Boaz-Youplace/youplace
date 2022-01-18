import json 

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf

spark = SparkSession\
        .builder\
        .appName('Python Spark SQL basic example')\
        .config('spark.some.config.option', 'some-value')\
        .getOrCreate()

# path 네임 [group_id]_[파티션0 기준 offset]으로 설정
test_path = './json_files/cars.json'
path = './json_files/test.json'

# 데이터프레임 생성
jeju_df = spark.read.json(path)    
jeju_df.printSchema()


# 스파크 데이터프레임에 SQL을 적용시킬 수 있는 객체 별도 생성
# jeju_df.createOrReplaceTempView("object_1")

gps = udf(lambda x: x[0])

# jeju_df.select(gps(jeju_df["x"])).show()
jeju_df.withColumn('x', gps(jeju_df["x"]))

# df2 = jeju_df.select('x', gps(jeju_df["x"]).alias('real_x'))
# print(df2)
#DataFrame[date_str: string, date: timestamp]

# jeju_df.show(truncate=False)
jeju_df.printSchema()

# df4.show(2)
# print(df4.schema) # 변경된 스키마 조회
# spark.sql("DESCRIBE object_1").show()