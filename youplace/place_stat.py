import json 
from pyspark.sql.functions import desc
import findspark

findspark.add_packages('mysql:mysql-connector-java:8.0.11')

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from decimal import Decimal
from pyspark.sql import types 
from pyspark.sql.functions import to_timestamp

spark = SparkSession\
        .builder\
        .appName('Python Spark SQL basic example')\
        .config('spark.some.config.option', 'some-value')\
        .getOrCreate()


# load data to a JDBC source
try:
    jdbcDF=spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://boaz-youplace.cai20ccufxe1.ap-northeast-2.rds.amazonaws.com:3306/?useSSL=false") \
    .option("dbtable", "db_youplace.tb_youplace") \
    .option("user", "admin") \
    .option("password", "youplace") \
    .option("numPartitions",5) \
    .option("driver","com.mysql.cj.jdbc.Driver",) \
    .load()
except Exception as e:
        # 대부분 중복 데이터(pk동일) 삽입에 대한 오류임 
        print(e)

print("complete to load data to rds-mysql")


# place_name기준으로 group_by 후 count
jdbcDF=jdbcDF.groupby("place_name").count()

# count 기준으로 정렬
jdbcDF.sort(desc("count")).show()