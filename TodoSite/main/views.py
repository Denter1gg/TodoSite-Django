from django.shortcuts import render


ASSETS_ROOT = "/static/assets"

def tables(request):

    context = {
        'ASSETS_ROOT' : ASSETS_ROOT,

    }
    return render(request, 'main/tables.html', context)

def create_task(request):

    context = {
        'ASSETS_ROOT' : ASSETS_ROOT,

    }
    return render(request, 'main/user.html', context)