from django.urls import path
from . import views


#app_name = 'eduGalaxy'

urlpatterns = [
    # the 'name' value as called by the {% url %} template tag
    path('', views.index, name='index'),
]

