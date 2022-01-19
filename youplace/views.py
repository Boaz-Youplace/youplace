from django.shortcuts import render

# Create your views here.

def view_map(request):
    return render(request, 'youplace/view_map.html', {})