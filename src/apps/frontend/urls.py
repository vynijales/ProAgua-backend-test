from django.urls import path, include

from . import views

urls_publicas = [
    path('visu_publica', views.visu_publica),
    path('', views.home),
    path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('lista_pontos/', views.lista_pontos),
]

urlpatterns = [
    # URLs públicas
    path('', include(urls_publicas)),

    # Pontos de coletas
    path('pontos/', views.pontos_coletas, name='visualizar_pontos'),
    path('pontos/<int:ponto_id>/', views.ponto_coleta, name='visualizar_ponto'),
    path('pontos/criar/', views.criar_ponto, name='criar_ponto'),
    path('pontos/<int:ponto_id>/', views.editar_ponto, name='editar_ponto'),
    path('pontos/<int:ponto_id>/amostragem/<int:amostragem>/', views.ponto_coleta_relatorio, name='visualizar_relatorio'),
    path('pontos/<int:ponto_id>/amostragem/criar', views.criar_amostragem, name='criar_amostragem'),

    # Coletas
    path('coletas/criar/', views.criar_coleta, name='criar_coleta'),
    path('coletas/<int:coleta_id>/', views.editar_coleta, name='editar_coleta'),

    # Edificacoes
    path('edificacoes/', views.edificacoes, name='visualizar_edificacoes'),
    path('edificacoes/criar/', views.criar_edificacao, name='criar_edificacao'),
    path('edificacoes/<str:cod_edificacao>/', views.edificacao, name='editar_edificacao'),
    path('edificacoes/<str:cod_edificacao>/excluir/', views.excluir_edificacao, name='excluir_edificacao'),

    # Usuários
    path('usuario/<int:id>/excluir', views.excluir_usuario, name='excluir_usuario'),

    # Sequencias de coletas
    path('sequencias_coletas/', views.sequencias_coletas),
    path('sequencias_coletas/<int:id>/', views.serve_protected_file('privado/sequencia_coletas.html')),
    path('sequencias_coletas/criar/', views.serve_protected_file('privado/criar_sequencia.html')),
    
    path('configuracoes/', views.configuracoes, name='configuracoes'),
]
