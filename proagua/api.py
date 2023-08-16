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
    edificacao = get_object_or_404(models.Edificacao, campus=cod_edificacao)
    edificacao.delete()
    return {"success": True}

# https://django-ninja.rest-framework.com/tutorial/other/crud/