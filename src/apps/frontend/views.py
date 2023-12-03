from django.shortcuts import (
    render,
    redirect
)

from django.contrib.auth.decorators import login_required


def serve_protected_file(file_name):
    @login_required
    def view(request):
        return render(
            request=request,
            template_name=file_name
        )
    
    return view


def serve_file(file_name, login_required=False):
    pass


def home(request):
    return render(
        request=request,
        template_name="landing_page.html"
    )

def password_reset(request):
    return render(
        request=request,
        template_name="registration/password_reset.html"
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
def sequencias_coletas(request):
    return render(
        request=request,
        template_name="privado/sequencias_coletas.html"
    )

@login_required
def pontos_coletas(request):
    return render(
        request=request,
        template_name="privado/pontos_coletas.html",
    )

@login_required
def criar_ponto(request):
    return render(
        request=request,
        template_name="privado/criar_ponto.html",
    )


@login_required
def editar_ponto(request, ponto_id: int):
    return render(
        request,
        'privado/editar_ponto.html',
    )


@login_required
def ponto_coleta(request, ponto_id: int):
    return render(
        request=request,
        template_name="privado/ponto_coleta.html",
    )


@login_required
def ponto_coleta_relatorio(request, ponto_id: int, amostragem: int):
    return render(
        request=request,
        template_name="privado/ponto_coleta_relatorio.html",
    )


@login_required
def criar_coleta(request):
    return render(
        request=request,
        template_name='privado/criar_coleta.html',
    )


@login_required
def criar_amostragem(request, ponto_id: int):
    return redirect(
        ponto_coleta,
    )


@login_required
def editar_coleta(request, coleta_id: int):
    return render(
        request=request,
        template_name='privado/editar_coleta.html',
    )


@login_required
def configuracoes(request):
    return render(
        request=request,
        template_name="privado/configuracoes.html",
    )


@login_required
def edificacoes(request):
    return render(
        request=request,
        template_name='privado/edificacoes.html',
    )


@login_required
def criar_edificacao(request):
    return render(
        request=request,
        template_name='privado/criar_edificacao.html',
    )


@login_required
def excluir_edificacao(request, edificacao_id: int):
    pass


@login_required
def edificacao(request, cod_edificacao: str):
    
    return render(
        request=request,
        template_name='privado/editar_edificacao.html'
    )

@login_required
def excluir_usuario(request, id:int):
    return redirect(configuracoes)
