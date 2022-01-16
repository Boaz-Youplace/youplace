from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import *
from pyspark.sql.functions import udf
from pyspark.sql.functions import col, pandas_udf, split

#sparkSession 생성
spark = SparkSession \
    .builder \
    .appName("service") \
    .getOrCreate()

# spark structured streaming을 이용
# kafka에서 데이터를 읽어와 dataframe 생성
df = spark \
    .readStream\
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("failOnDataLoss","False") \
    .option("subscribe", "test0113") \
    .load()

print(df.count())
print(df.show())