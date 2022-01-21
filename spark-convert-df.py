#encoding : utf-8
import json 
import findspark

findspark.add_packages('mysql:mysql-connector-java:8.0.11')

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from decimal import Decimal
from pyspark.sql import types 
from pyspark.sql.functions import to_timestamp

# pyspark에서 지원하는 타입 확인
for t in ['BinaryType', 'BooleanType', 'ByteType', 'DateType', 
          'DecimalType', 'DoubleType', 'FloatType', 'IntegerType', 
           'LongType', 'ShortType', 'StringType', 'TimestampType']:
        print(f"{t}: {getattr(types, t)().simpleString()}")


spark = SparkSession\
        .builder\
        .appName('Python Spark SQL basic example')\
        .config('spark.some.config.option', 'some-value')\
        .getOrCreate()

# path 네임 [group_id]_[파티션0 기준 offset]으로 설정
path = './json_files/test.json'

# 데이터프레임 생성
df = spark.read.json(path)   

# 형태변환 작업 정 print스키마
df.printSchema()
# 배열 내 요소 추출 함수 (udf 사용)
extract_element = udf(lambda x: x[0])

# udf 적용
df=df.withColumn('x', extract_element(df["x"]))
df=df.withColumn('y', extract_element(df["y"]))
df=df.withColumn('place_name', extract_element(df["place_name"]))

# casting

# 1) string to int
df = df.withColumn("likeCount", df["likeCount"].cast("int"))
df = df.withColumn("viewCount", df["viewCount"].cast("int"))

# 2) string to decimal
df = df.withColumn("x", df["x"].cast("decimal(24,18)"))
df = df.withColumn("y", df["y"].cast("decimal(24,18)"))

# 3) string to timestamp
df = df.withColumn("publishTime", df["publishTime"].cast("timestamp"))

df.printSchema()

df.show(5)

# 중복 확인 함수 - 존재하면 jdbc write 과정 중 오류 남  !! (중요)
df=df.groupby(['id', 'place_name']) \
    .count() \
    .where('count > 1') \
    .sort('count', ascending=False) \
    .show()


# Saving data to a JDBC source
try:
        df.write \
        .format("jdbc") \
        .option("url", "jdbc:mysql://boaz-youplace.cai20ccufxe1.ap-northeast-2.rds.amazonaws.com:3306/?useSSL=false") \
        .option("dbtable", "db_youplace.tb_youplace") \
        .option("user", "admin") \
        .option("password", "youplace") \
        .option("numPartitions",5) \
        .option("driver","com.mysql.cj.jdbc.Driver",) \
        .mode('append') \
        .save()
        
except Exception as e:
        # 대부분 중복 데이터(pk동일) 삽입에 대한 오류임 
        print('fail')
        print(e)

