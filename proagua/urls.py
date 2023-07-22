from django.urls import path, include
from . import views

ponto_coleta_urls = [
    path('', views.pontos_coletas, name='visualizar_pontos'),
    path('<int:ponto_id>/', views.ponto_coleta, name='visualizar_ponto'),
    path('<int:ponto_id>/editar', views.editar_ponto, name='editar_ponto'),
    path('<int:ponto_id>/amostragem/<int:amostragem>/', views.ponto_coleta_relatorio, name='visualizar_relatorio'),
    path('<int:ponto_id>/amostragem/criar', views.criar_amostragem, name='criar_amostragem'),
    path('criar/', views.criar_ponto, name='criar_ponto'),
]

coleta_urls = [
    path('criar/', views.criar_coleta, name='criar_coleta'),
    path('<int:coleta_id>/editar/', views.editar_coleta, name='editar_coleta')
]

edificacao_urls = [
    path('', views.edificacoes, name='visualizar_edificacoes'),
    path('<int:edificacao_id>/editar/', views.edificacao, name='editar_edificacao'),
    path('<int:edificacao_id>/excluir/', views.excluir_edificacao, name='excluir_edificacao'),
    path('criar/', views.criar_edificacao, name='criar_edificacao'),
]

accounts_urls = [
    path('<int:id>/excluir', views.excluir_usuario, name='excluir_usuario'),
]

urlpatterns = [
    path('', views.home),
    path('ponto/', include(ponto_coleta_urls)),
    path('coleta/', include(coleta_urls)),
    path('edificacao/', include(edificacao_urls)),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include(accounts_urls)),
]
