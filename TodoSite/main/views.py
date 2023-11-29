from django.shortcuts import render

def tables(request):
    return render(request, 'main/tables.html', )