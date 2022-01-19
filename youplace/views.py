from django.shortcuts import render
from youplace.models import TbYouplace
# using을 이용해 앞서 설정한 external 이름을 넣어주면 된다.
import json
from place_stat import load_data,groupby_count,print_df,spark

# Create your views here.
 
def main(request):
    queryset = TbYouplace.objects.all()
    return render(request,'youplace/main.html',{'datas':queryset})

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