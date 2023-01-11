from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about', views.about, name='blog-about'),
]