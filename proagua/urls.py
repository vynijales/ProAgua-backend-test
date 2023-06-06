from django.urls import path, include
from . import views
from .api import api

urlpatterns = [
    path('', views.home),
    path('pontos_coletas/', views.pontos_coletas),
    path('accounts/', include('django.contrib.auth.urls')),
]