from typing import List

from django.shortcuts import get_object_or_404
from django.urls import reverse
from ninja import NinjaAPI
from ninja.security import django_auth

from .schema import *
from . import models

api = NinjaAPI(auth=django_auth, csrf=True)

@api.get("/edificacoes", response=List[EdificacaoOut])
def list_edificacoes(request):
    qs = models.Edificacao.objects.all()
    return qs

@api.get("/edificacoes/{cod_edificacao}", response=EdificacaoOut)
def get_edificacao(request, cod_edificacao: str):
    qs = get_object_or_404(models.Edificacao, codigo=cod_edificacao)
    return qs

@api.post("/edificacoes")
def create_edificacao(request, payload: EdificacaoIn):
    edificacao = models.Edificacao.objects.create(**payload.dict())
    return {"success": True}

@api.put("/edificacoes/{cod_edificacao}")
def update_edificacoes(request, cod_edificacao: str, payload: EdificacaoIn):
    edificacao = get_object_or_404(models.Edificacao, codigo=cod_edificacao)
    for attr, value in payload.dict().items():
        setattr(edificacao, attr, value)
    edificacao.save()
    return {"success": True}

@api.delete("/edificacoes/{cod_edificacao}")
def delete_edificacao(request, cod_edificacao: str):
    edificacao = get_object_or_404(models.Edificacao, codigo=cod_edificacao)
    edificacao.delete()
    return {"success": True}

################################################################

@api.get("/pontos", response=List[PontoColetaOut])
def list_ponto(request):
    qs = models.PontoColeta.objects.all()
    return qs

@api.get("/pontos/{id_ponto}", response=PontoColetaOut)
def get_ponto(request, id_ponto: int):
    qs = get_object_or_404(models.PontoColeta, id=id_ponto)
    return qs

@api.post("/pontos", response=PontoColetaOut)
def create_ponto(request, payload: PontoColetaIn):
    edificacao = get_object_or_404(models.Edificacao, codigo=payload.edificacao_codigo)

    data_dict = payload.dict()
    data_dict.pop("edificacao_codigo")
    data_dict["edificacao"] = edificacao

    qs = models.PontoColeta.objects.create(**data_dict)

    return qs

@api.put("/pontos/{id_ponto}")
def update_ponto(request, id_ponto: int, payload: PontoColetaIn):
    ponto = get_object_or_404(models.PontoColeta, id=id_ponto)
    for attr, value in payload.dict().items():
        setattr(ponto, attr, value)
    ponto.save()
    return {"success": True}

@api.delete("/pontos/{id_ponto}")
def delete_ponto(request, id_ponto: int):
    ponto = get_object_or_404(models.PontoColeta, id=id_ponto)
    ponto.delete()
    return {"success": True}

# https://django-ninja.rest-framework.com/tutorial/other/crud/
# https://django-ninja.rest-framework.com/guides/response/?h=resolvers#resolvers