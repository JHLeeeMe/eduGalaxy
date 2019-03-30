from django.shortcuts import render


def index(request):
    return render(request, 'eduGalaxy/index.html', {})


def sign_up(request):
    return render(request, 'regsistration/sign_up.html', {})


