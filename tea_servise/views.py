from django.shortcuts import render


def index(request):
    return render(request, 'tea_dervise/index.html')
