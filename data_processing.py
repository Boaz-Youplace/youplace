# 실제 실행시키는 파일 & 데이터 전처리 

from pprint import pprint
from collecting_data import collect_data

q='제주 vlog'
order='date'

pprint(collect_data(q,order))