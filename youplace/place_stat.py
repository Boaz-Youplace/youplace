import json
from venv import create 
from pyspark.sql.functions import desc
import findspark

findspark.add_packages('mysql:mysql-connector-java:8.0.11')

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from decimal import Decimal
from pyspark.sql import types 
from pyspark.sql.functions import to_timestamp

def create_session():
    spark = SparkSession\
            .builder\
            .appName('Python Spark SQL basic example')\
            .config('spark.some.config.option', 'some-value')\
            .getOrCreate()
    return spark
    
def sql_limit_10(df):
    df=df.createOrReplaceTempView("tmp_df")
    df=create_session().sql("SELECT * FROM tmp_df LIMIT 10")
    df.show()
    return df

def load_data(spark):
    # load data to a JDBC source
    try:
        jdbcDF=spark.read \
        .format("jdbc") \
        .option("url", "jdbc:mysql://boaz-youplace.cai20ccufxe1.ap-northeast-2.rds.amazonaws.com:3306/?useSSL=false") \
        .option("dbtable", "db_youplace.tb_youplace") \
        .option("user", "admin") \
        .option("password", "youplace") \
        .option("numPartitions",20) \
        .option("driver","com.mysql.cj.jdbc.Driver",) \
        .load()
    except Exception as e:
            # 대부분 중복 데이터(pk동일) 삽입에 대한 오류임 
            print(e)

    print("complete to load data to rds-mysql")

    return jdbcDF

def basic_groupby(df,column):
    df=df.groupby(column)
    df.show(5)
    return df

def groupby_count(df,column):
    # place_name기준으로 group_by 후 count
    df=df.groupby(column).count()
    # count 기준으로 정렬
    df=df.sort(desc("count"))
    df.show(5)
    return df

def print_df(df):
    df.show()
    
if __name__=='__main__':
    # place_name_df=groupby_count(load_data(spark),"place_name")
    # sql_limit_10(place_name_df)

    # categpry_df=groupby_count(load_data(spark),"category")
    # sql_limit_10(categpry_df)
    
    # lala=groupby_count(load_data(spark),"id")

    address_df=groupby_count(load_data(create_session()),"address_6")
    sql_limit_10(address_df)