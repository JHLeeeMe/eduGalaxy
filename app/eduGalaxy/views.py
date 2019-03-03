from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CreateUserForm


# Create your views here.
def index(request):
    return render(request, 'eduGalaxy/index.html', {})


class CreateUserView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('index')

