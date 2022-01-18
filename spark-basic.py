import json 

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from decimal import Decimal

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

df=df.withColumn('x', extract_element(df["x"]))
df=df.withColumn('y', extract_element(df["y"]))
df=df.withColumn('place_name', extract_element(df["place_name"]))

# 형 변환 함수 (udf 사용)
convertStringToInt= udf(lambda x:int(x)) #likeCount,viewCount 사용
convertStringToDecimal= udf(lambda x:Decimal(x)) #x,y

df.printSchema()

print(3)
df=df.withColumn('likeCount', convertStringToInt(df["likeCount"]))
df=df.withColumn('viewCount', convertStringToInt(df["viewCount"]))
df=df.withColumn('x', convertStringToDecimal(df["x"]))
df=df.withColumn('y', convertStringToDecimal(df["y"]))

df.printSchema()

# 스파크 데이터프레임에 SQL을 적용시킬 수 있는 객체(for 통계처리) 별도 생성
# df.createOrReplaceTempView("object_1")
# spark.sql("DESCRIBE object_1").show()