# pyspark 실행 및 예문 따라하는 기초 파일입니다.
from pprint import pprint
import pyspark
pyspark.__version__

from pyspark import SparkConf, SparkContext

# 1. sparkContext라는 객체선언 (엔트리포인트)

sc=SparkContext(master='local',appName='pySpark Basic')
print(sc)

print(sc.getConf().getAll())