from django.urls import path

from . import views


urlpatterns = [ 
    path('', views.embed, name='embed'),
]