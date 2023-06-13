from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.db.models import Count

from .models import (
    PontoColeta,
    Coleta
)
from .forms import (
    CreatePontoColeta,
    CreateColeta
)

def home(request):
    return render(
        request=request,
        template_name="landing_page.html"
    )


def pontos_coletas(request):
    context = {
        'pontos_coletas': PontoColeta.objects.all(),
    }

    return render(
        request=request,
        template_name="privado/pontos_coletas.html",
        context=context
    )


def criar_ponto(request):
    if request.method == 'POST':
        form = CreatePontoColeta(request.POST)
        form.save()
    form = CreatePontoColeta()

    return render(
        request=request,
        template_name="privado/criar_ponto.html",
        context={ 'form': form }
    )
def ponto_coleta(request, ponto_id: int):
    ponto = get_object_or_404(
        PontoColeta,
        id=ponto_id
    )

    count = ponto.coletas.aggregate(Count("amostragem", distinct=True))

    context = {
        "amostragens": range(1, count["amostragem__count"] + 1),
        "ponto": ponto
    }

    return render(
        request=request,
        template_name="privado/ponto_coleta.html",
        context=context
    )


def ponto_coleta_relatorio(request, ponto_id: int, amostragem: int):
    ponto = get_object_or_404(
        PontoColeta,
        id=ponto_id
    )
    pontos = []
    
    while ponto != None:
        coletas = ponto.coletas.filter(amostragem=amostragem)
        
        if coletas.count() == 0:
            break

        pontos.append({
            "edificacao": ponto.edificacao,
            "ambiente": ponto.ambiente,
            "coletas": coletas
        })
        ponto = ponto.pai

    context = {
        "pontos": pontos,
    }

    return render(
        request=request,
        template_name="privado/ponto_coleta_relatorio.html",
        context=context
    )


def criar_coleta(request):
    if request.method == 'POST':
        coleta = Coleta()
        # coleta.ponto_coleta = ponto
        form = CreateColeta(request.POST, instance=coleta)
        form.save()
    form = CreateColeta()
    
    return render(
        request=request,
        template_name='privado/criar_coleta.html',
        context={ 'form': form }
    )


def configuracoes(request):
    context = {
        'users': User.objects.all()
    }
    return render(
        request=request,
        template_name="privado/configuracoes.html",
        context=context
    )
