from django.urls import path

from . import views


urlpatterns = [ 
    path('', views.embed, name='embed'),
    path('invite/', views.invite, name='invite'),
    path('zoom/', views.ImgZoom, name='zoom'),
    path('fritzing/', views.fritzing, name='fritzing'),
]