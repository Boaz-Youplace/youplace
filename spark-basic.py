import json 

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from decimal import Decimal
from pyspark.sql import types 

# pyspark에서 지원하는 타입 확인
for t in ['BinaryType', 'BooleanType', 'ByteType', 'DateType', 
          'DecimalType', 'DoubleType', 'FloatType', 'IntegerType', 
           'LongType', 'ShortType', 'StringType', 'TimestampType']:
        print(f"{t}: {getattr(types, t)().simpleString()}")

'''
BinaryType: binary
BooleanType: boolean
ByteType: tinyint
DateType: date
DecimalType: decimal(10,0)
DoubleType: double
FloatType: float
IntegerType: int
LongType: bigint
ShortType: smallint
StringType: string
TimestampType: timestamp
'''

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
df.show(5)

print("after")

# 배열 내 요소 추출 함수 (udf 사용)
extract_element = udf(lambda x: x[0])

# udf 적용
df=df.withColumn('x', extract_element(df["x"]))
df=df.withColumn('y', extract_element(df["y"]))
df=df.withColumn('place_name', extract_element(df["place_name"]))

# casting
df = df.withColumn("likeCount", df["likeCount"].cast("int"))
df = df.withColumn("viewCount", df["viewCount"].cast("int"))
df = df.withColumn("x", df["x"].cast("decimal(24,18)"))
df = df.withColumn("y", df["y"].cast("decimal(24,18)"))


df.printSchema()

# 스파크 데이터프레임에 SQL을 적용시킬 수 있는 객체(for 통계처리) 별도 생성
# df.createOrReplaceTempView("object_1")
# spark.sql("DESCRIBE object_1").show()