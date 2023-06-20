from django.shortcuts import (
    render,
    get_object_or_404,
    HttpResponseRedirect
)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.forms import ChoiceField

from .models import (
    PontoColeta,
    Coleta,
    Edificacao
)
from .forms import (
    FormPontoColeta,
    FormColeta,
    FormEdificacao,
)

from .utils import get_hierarquia


def home(request):
    return render(
        request=request,
        template_name="landing_page.html"
    )


@login_required
def pontos_coletas(request):
    # Retornar somente bebedouros e torneiras
    pontos = PontoColeta.objects.filter(tipo__in=['BE', 'TO'])
    context = {
        'pontos_coletas': pontos,
    }

    return render(
        request=request,
        template_name="privado/pontos_coletas.html",
        context=context
    )


@login_required
def criar_ponto(request):
    if request.method == 'POST':
        form = FormPontoColeta(request.POST)
        form.save()
    form = FormPontoColeta()

    return render(
        request=request,
        template_name="privado/criar_ponto.html",
        context={ 'form': form }
    )


@login_required
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


@login_required
def ponto_coleta_relatorio(request, ponto_id: int, amostragem: int):
    ponto = get_object_or_404(
        PontoColeta,
        id=ponto_id
    )

    context = {
        "pontos": get_hierarquia(ponto, amostragem),
        "amostragem": amostragem,
    }

    return render(
        request=request,
        template_name="privado/ponto_coleta_relatorio.html",
        context=context
    )


@login_required
def criar_coleta(request):
    ponto_id = request.GET.get('p')
    amostragem = request.GET.get('amostragem')
    ponto = PontoColeta.objects.get(id = int(ponto_id))

    if request.method == 'POST':
        # form = FormColeta(request.POST, pontos = get_hierarquia(ponto, amostragem))
        form = FormColeta(request.POST)
        form.save()

        next_url = request.GET.get('next')
        if next_url:
            return HttpResponseRedirect(next_url)
    
    pontos = get_hierarquia(ponto, amostragem)
    # print(f"PONTOS 110: {pontos}")

    form = FormColeta()
    #teste
    if pontos:
        choices = [(p['id'], p['nome']) for p in pontos]
        # print(f"CHOICES 116: {choices}")
        form.fields['ponto_coleta'] = ChoiceField(choices=choices)
    
    return render(
        request=request,
        template_name='privado/criar_coleta.html',
        context={ 'form': form }
    )


@login_required
def editar_coleta(request, coleta_id: int):
    coleta = Coleta.objects.get(id=coleta_id)
    form = FormColeta(instance=coleta)

    if request.method == 'POST':
        form = FormColeta(request.POST, instance=coleta)
        form.save()

        next_url = request.GET.get('next')
        if next_url:
            return HttpResponseRedirect(next_url)


    return render(
        request=request,
        template_name='privado/editar_coleta.html',
        context={ 'form': form }
    )


@login_required
def configuracoes(request):
    context = {
        'users': User.objects.all()
    }
    return render(
        request=request,
        template_name="privado/configuracoes.html",
        context=context
    )


@login_required
def edificacoes(request):
    search = request.GET.get("q")
    if search:
        edificacoes = Edificacao.objects.filter(
            Q(nome__contains=search) | Q(codigo__contains=search)
        )
    else:
        edificacoes = Edificacao.objects.all()

    context = {
        'edificacoes': edificacoes
    }

    return render(
        request=request,
        template_name='privado/edificacoes.html',
        context=context
    )


@login_required
def criar_edificacao(request):
    if request.method == 'POST':
        form = FormEdificacao(request.POST)
        form.save()
    form = FormEdificacao()

    return render(
        request=request,
        template_name='privado/criar_edificacao.html',
        context={ 'form': form}
    )
