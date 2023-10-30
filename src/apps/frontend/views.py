from django.shortcuts import (
    render,
    # get_object_or_404,
    # HttpResponseRedirect,
    redirect
)

# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# from django.db.models import Count, Q
# from django.forms import ChoiceField

# from .models import (
#     PontoColeta,
#     Coleta,
#     Edificacao,
#     SequenciaColetas
# )

# from .forms import (
#     FormPontoColeta,
#     FormColeta,
#     FormEdificacao,
#     FormSearchPontos,
# )

# from .utils import get_hierarquia


def home(request):
    return render(
        request=request,
        template_name="landing_page.html"
    )

def visu_publica(request):
    return render(
        request=request,
        template_name="visu_publica.html"
    )

def lista_pontos(request):
    return render(
        request=request,
        template_name="lista_pontos.html"
    )

@login_required
def pontos_coletas(request):
    # search = request.GET.get("q")
    # form_search = FormSearchPontos(request.GET)
    # pontos = PontoColeta.objects

    # if search:
    #     pontos = pontos.filter(
    #         Q(edificacao__nome__contains=search)
    #     )
    # q = Q()

    # if form_search.is_valid():
    #     if form_search.cleaned_data.get("campus"):
    #         q &= Q(edificacao__campus = form_search.cleaned_data["campus"])
    #     if form_search.cleaned_data.get("tipo"):
    #         q &= Q(tipo__in = form_search.cleaned_data["tipo"])
        
    #     if form_search.cleaned_data.get("data_minima"):
    #         q &= Q(coletas__date__gt = form_search.cleaned_data["data_minima"])

    #     if form_search.cleaned_data.get("data_maxima"):
    #         q &= Q(coletas__date__lt = form_search.cleaned_data["data_maxima"])

    # pontos = pontos.filter(q)
    # context = {
    #     'pontos_coletas': pontos,
    #     'form_search': form_search,
    # }

    return render(
        request=request,
        template_name="pontos_coletas_teste.html",
        # context=context
    )

@login_required
def criar_ponto(request):
    # if request.method == 'POST':
    #     form = FormPontoColeta(request.POST)
    #     form.save()
    # form = FormPontoColeta()

    return render(
        request=request,
        template_name="privado/criar_ponto.html",
        # context={ 'form': form }
    )


@login_required
def editar_ponto(request, ponto_id: int):
    # ponto = get_object_or_404(
    #     PontoColeta,
    #     id=ponto_id
    # )

    # if request.method == 'POST':
    #     form = FormPontoColeta(request.POST, instance=ponto)
    #     if form.is_valid():
    #         form.save()
    #         return redirect(pontos_coletas)
    # else:
    #     form = FormPontoColeta(instance=ponto)

    return render(
        request,
        'privado/editar_ponto.html',
        # {'form': form}
    )


@login_required
def ponto_coleta(request, ponto_id: int):
    # ponto = get_object_or_404(
    #     PontoColeta,
    #     id=ponto_id
    # )

    # context = {
    #     "ponto": ponto
    # }

    return render(
        request=request,
        template_name="privado/ponto_coleta.html",
        # context=context
    )


@login_required
def ponto_coleta_relatorio(request, ponto_id: int, amostragem: int):
    # ponto = get_object_or_404(
    #     PontoColeta,
    #     id=ponto_id
    # )

    # context = {
    #     "pontos": get_hierarquia(ponto, amostragem),
    #     "amostragem": amostragem,
    # }

    return render(
        request=request,
        template_name="privado/ponto_coleta_relatorio.html",
        # context=context
    )


@login_required
def criar_coleta(request):
    # ponto_id = request.GET.get('p')
    # amostragem = request.GET.get('amostragem')
    # ponto = PontoColeta.objects.get(id = int(ponto_id))

    # if request.method == 'POST':
    #     form = FormColeta(request.POST)
    #     form.save()

    #     next_url = request.GET.get('next')
    #     if next_url:
    #         return HttpResponseRedirect(next_url)
    
    # pontos = get_hierarquia(ponto, amostragem)

    # form = FormColeta(initial={
    #     'amostragem': amostragem
    # })
    
    # if pontos:
    #     choices = [(p['id'], p['nome']) for p in pontos]
    #     form.fields['ponto_coleta'] = ChoiceField(choices=choices)
    
    return render(
        request=request,
        template_name='privado/criar_coleta.html',
        # context={ 'form': form }
    )


@login_required
def criar_amostragem(request, ponto_id: int):
    # ponto = get_object_or_404(
    #     PontoColeta,
    #     id=ponto_id
    # )
    # amostragem, created = Amostragem.objects.get_or_create(
    #     amostragem=ponto.amostragens.count() + 1
    # )
    # ponto.amostragens.add(amostragem)
    return redirect(
        ponto_coleta,
        # ponto_id=ponto_id
    )


@login_required
def editar_coleta(request, coleta_id: int):
    # coleta = Coleta.objects.get(id=coleta_id)
    # form = FormColeta(instance=coleta)

    # if request.method == 'POST':
    #     form = FormColeta(request.POST, instance=coleta)
    #     form.save()

    #     next_url = request.GET.get('next')
    #     if next_url:
    #         return HttpResponseRedirect(next_url)
    
    return render(
        request=request,
        template_name='privado/editar_coleta.html',
        # context={ 'form': form }
    )


@login_required
def configuracoes(request):
    # context = {
    #     'users': User.objects.all()
    # }
    return render(
        request=request,
        template_name="privado/configuracoes.html",
        # context=context
    )


@login_required
def edificacoes(request):
    # search = request.GET.get("q")
    # if search:
    #     edificacoes = Edificacao.objects.filter(
    #         Q(nome__contains=search) | Q(codigo__contains=search)
    #     )
    # else:
    #     edificacoes = Edificacao.objects.all()

    # context = {
    #     'edificacoes': edificacoes
    # }

    return render(
        request=request,
        template_name='privado/edificacoes.html',
        # context=context
    )


@login_required
def criar_edificacao(request):
    # if request.method == 'POST':
    #     form = FormEdificacao(request.POST)
    #     form.save()
    # form = FormEdificacao()

    return render(
        request=request,
        template_name='privado/criar_edificacao.html',
        # context={ 'form': form}
    )


@login_required
def excluir_edificacao(request, edificacao_id: int):
    pass


@login_required
def edificacao(request, edificacao_id: int):
    # edificacao = get_object_or_404(Edificacao, id=edificacao_id)
    # form = FormEdificacao(instance=edificacao)
    
    # if request.method == 'POST':
    #     form = FormEdificacao(request.POST, instance=edificacao)
    #     form.save()

    #     next_url = request.GET.get('next')
    #     if next_url:
    #         return HttpResponseRedirect(next_url)

    
    return render(
        request=request,
        template_name='privado/editar_edificacao.html',
        # context={ 'edificacao': edificacao, 'form': form }
    )

@login_required
def excluir_usuario(request, id:int):
    # if request.POST:
    #     User.objects.filter(pk=id).delete()
    return redirect(configuracoes)