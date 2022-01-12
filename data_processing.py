# 실제 실행시키는 파일 & 데이터 전처리 

from pprint import pprint
from collecting_data import collect_data

# 인자 형식은 모두 string입니당 !
q='제주 vlog'
order='date'
publishedBefore=''
publishedAfter=''

dataset = collect_data(q,order)
pprint(collect_data(q,order))

#dataset 가지고 데이터 전처리 쭈욱 진행하면 될 것 같아융 (❁´◡`❁) !