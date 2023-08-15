from typing import List

from django.shortcuts import get_object_or_404
from ninja import NinjaAPI

from .schema import *
from . import models

api = NinjaAPI()

@api.post("/edificacoes")
def create_edificacao(request, payload: EdificacaoIn):
    edificacao = models.Edificacao.objects.create(**payload.dict())
    return {
        'codigo': edificacao.codigo,
        'nome': edificacao.nome,
        'campus': edificacao.nome}

@api.get("/edificacoes", response=List[EdificacaoOut])
def list_edificacoes(request):
    qs = models.Edificacao.objects.all()
    return qs

@api.put("/edificacoes/{cod_edificacao}")
def update_edificacoes(request, cod_edificacao: str, payload: EdificacaoIn):
    edificacao = get_object_or_404(models.Edificacao, codigo=cod_edificacao)
    for attr, value in payload.dict().items():
        setattr(edificacao, attr, value)
    edificacao.save()
    return {"success": True}

@api.delete("/edificacoes/{cod_edificacao}")
def delete_edificacao(request, cod_edificacao: str):
    edificacao = get_object_or_404(models.Edificacao, campus=cod_edificacao)
    edificacao.delete()
    return {"success": True}

# https://django-ninja.rest-framework.com/tutorial/other/crud/