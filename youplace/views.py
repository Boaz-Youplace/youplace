from django.shortcuts import render
from youplace.models import TbYouplace
# using을 이용해 앞서 설정한 external 이름을 넣어주면 된다.
import json
import pandas as pd
from youplace.place_stat import load_data,groupby_count,sql_limit_10,create_session
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.core import serializers
from django.http import JsonResponse

# Create your views here.
 
def main(request):
    videos = TbYouplace.objects.filter(address_6='애월,한림,한경(제주시 서부)').order_by('-viewcount')[:5]
    videoJson =serializers.serialize('json',videos)
    context = {
        'videoJson':videoJson
    }
    return render(request,'youplace/main.html', context)

def video(request):
    videos = TbYouplace.objects.filter(address_6='애월,한림,한경(제주시 서부)').order_by('-viewcount')[:5]
    videoJson =serializers.serialize('json',videos)
    context = {
        'videoJson':videoJson
    }
    return render(request,'youplace/video.html',context)

def video_detail(request, pk):
    video = get_object_or_404(TbYouplace, pk=pk)
    return render(request, 'youplae/video_detail.html', {'video':video})

def view_map_gm(request):
    queryset = TbYouplace.objects.all()
    return render(request, 'youplace/view_map_gm.html', {'datas':queryset})

def view_map_jh(request):
    queryset = TbYouplace.objects.all()
    return render(request, 'youplace/view_map_jh.html', {'datas':queryset})

def view_map_es(request):
    return render(request, 'youplace/view_map_es.html', )



    # place_name_df=sql_limit_10(groupby_count(load_data(create_session()),"place_name"))
    # place_names = list(place_name_df.select('place_name').toPandas()['place_name'])
    # counts = list(place_name_df.select('count').toPandas()['count'])
    # p_ranks=[]
    # for place_name,count in zip(place_names,counts):
    #     p_ranks.append({'place_name':place_name,'count':count})

    # category_df=sql_limit_10(groupby_count(load_data(create_session()),"category"))
    # categorys = list(category_df.select('category').toPandas()['category'])
    # counts = list(category_df.select('count').toPandas()['count'])
    # c_ranks=[]
    # for category,count in zip(categorys,counts):
    #     c_ranks.append({'place_name':category, 'count':count})

    # context = {
    #     'p_ranks':p_ranks,
    #     'c_ranks':c_ranks,
    #     'videos':videos
    # }
    # videoJson = json.dumps(videos, ensure_ascii=False)