from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home),
    path('pontos_coletas/', views.pontos_coletas, name='admin_pontos_coletas'),
    path('ponto_coleta/<int:ponto_id>/', views.ponto_coleta, name='admin_ponto_coleta'),
    path('ponto_coleta/<int:ponto_id>/<int:amostragem>/', views.ponto_coleta_relatorio, name='admin_ponto_coleta_amostragem'),
    path('accounts/', include('django.contrib.auth.urls')),
]
