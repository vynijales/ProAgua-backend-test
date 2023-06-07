from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home),
    path('pontos_coletas/', views.pontos_coletas),
    path('ponto_coleta/<int:ponto_id>/<int:amostragem>', views.ponto_coleta_relatorio),
    path('accounts/', include('django.contrib.auth.urls')),
]
