from django.urls import path
from . import views
from .models import *

urlpatterns = [
    path('index.html', views.account, name="index"),
    path('list-card.html', views.list_card, name="list_card"),
    path('home/', views.home, name = "home"),
]