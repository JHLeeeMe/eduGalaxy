from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import EduGalaxyUserCreationForm


# Create your views here.
def index(request):
    return render(request, 'eduGalaxy/index.html', {})


class EduGalaxyUserCreateView(CreateView):
    template_name = 'registration/signup.html'
    form_class = EduGalaxyUserCreationForm
    success_url = reverse_lazy('resistration/login.html')

