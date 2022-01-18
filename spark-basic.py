import json 

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


# Saving data to a JDBC source
# df.write \
#     .format("jdbc") \
#     .option("url", "jdbc:mysql://boaz-youplace.cai20ccufxe1.ap-northeast-2.rds.amazonaws.com:3306") \
#     .option("dbtable", "db_youplace.spark_youplace") \
#     .option("user", "admin") \
#     .option("password", "youplace") \
#     .option("driver","com.mysql.jdbc.Driver",) \
#     .option("numPartitions",5,) \
#     .option("partitionColumn","id",) \
#     .option("createTableColumnTypes","address_6 VARCHAR(32) , category VARCHAR(32) , id VARCHAR(32) not null , likeCount INT , place_name VARCHAR(50) not null , place_url VARCHAR(100) , publishTime varchar(50) , viewCount INT , x DECIMAL(24,18) , x DECIMAL(24,18) , primary key(id,place_name) ") 
#     .mode('append') \
#     .save()

# # Specifying create table column data types on write
# df.write \
#     .option("createTableColumnTypes", "name CHAR(64), comments VARCHAR(1024)") \
#     .jdbc("jdbc:postgresql:dbserver", "schema.tablename",
#           properties={"user": "username", "password": "password"})

# # 스파크 데이터프레임에 SQL을 적용시킬 수 있는 객체(feat. 통계처리) 별도 생성

# # 1) 