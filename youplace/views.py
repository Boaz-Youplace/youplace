from django.shortcuts import render
from youplace.models import TbYouplace
# using을 이용해 앞서 설정한 external 이름을 넣어주면 된다.
import json
import pandas as pd
from youplace.place_stat import load_data,groupby_count,sql_limit_10,spark

# Create your views here.
 
def main(request):
    videos = TbYouplace.objects.all()

    place_name_df=sql_limit_10(groupby_count(load_data(spark),"place_name"))
    place_names = list(place_name_df.select('place_name').toPandas()['place_name'])
    counts = list(place_name_df.select('count').toPandas()['count'])
    p_ranks=[]
    for place_name,count in zip(place_names,counts):
        p_ranks.append({'place_name':place_name,'count':count})

    category_df=sql_limit_10(groupby_count(load_data(spark),"category"))
    categorys = list(category_df.select('category').toPandas()['category'])
    counts = list(category_df.select('count').toPandas()['count'])
    c_ranks=[]
    for category,count in zip(categorys,counts):
        c_ranks.append({'place_name':category, 'count':count})

    context = {
        'p_ranks':p_ranks,
        'c_ranks':c_ranks,
        'videos':videos
    }
    return render(request,'youplace/main.html', context)

def view_map_gm(request):
    queryset = TbYouplace.objects.all()
    return render(request, 'youplace/view_map_gm.html', {'datas':queryset})

def view_map_jh(request):
    queryset = TbYouplace.objects.all()
    return render(request, 'youplace/view_map_jh.html', {'datas':queryset})

def view_map_es(request):
    queryset = TbYouplace.objects.all()

    query = {
        'x': 126.345010602598690000,
        'y': 33.396700480684250000,
        'place_name': '아르떼뮤지엄 제주'
    }
    queryJson = json.dumps(query)
    return render(request, 'youplace/view_map_es.html', {'all':queryset,'queryJson':queryJson})