from django.shortcuts import render

# Create your views here.

def view_map_gm(request):
    return render(request, 'youplace/view_map_gm.html', {})

def view_map_jh(request):
    return render(request, 'youplace/view_map_jh.html', {})

def view_map_es(request):
    return render(request, 'youplace/view_map_es.html', {})