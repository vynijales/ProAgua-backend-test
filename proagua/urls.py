from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('coletas/', views.coletas),
    path('accounts/', include('django.contrib.auth.urls'))
]