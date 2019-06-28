from django.urls import path
from . import views


urlpatterns = [
    # the 'name' value as called by the {% url %} template tag
    path('', views.index, name='index'),
    path('sign_up/', views.sign_up, name='sign_up'),
]

