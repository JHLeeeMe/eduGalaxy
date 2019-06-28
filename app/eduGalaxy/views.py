from django.shortcuts import render
from .forms import EduGalaxySignupForm

def index(request):
    return render(request, 'eduGalaxy/index.html', {})


def sign_up(request):
    SignupForm = EduGalaxySignupForm()

    return render(request, 'regsistration/sign_up.html', {'SignupForm': SignupForm})



