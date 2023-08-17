from typing import List

from django.shortcuts import get_object_or_404
from django.urls import reverse
from ninja import NinjaAPI, Router
from ninja.security import django_auth

from .schema import *
from proagua import models

# api = NinjaAPI(auth=django_auth, csrf=True)
router = Router()

@router.get("/", response=List[PontoColetaOut])
def list_ponto(request):
    qs = models.PontoColeta.objects.all()
    return qs

@router.get("/{id_ponto}", response=PontoColetaOut)
def get_ponto(request, id_ponto: int):
    qs = get_object_or_404(models.PontoColeta, id=id_ponto)
    return qs

@router.post("/", response=PontoColetaOut)
def create_ponto(request, payload: PontoColetaIn):
    edificacao = get_object_or_404(models.Edificacao, codigo=payload.edificacao_codigo)

    data_dict = payload.dict()
    data_dict.pop("edificacao_codigo")
    data_dict["edificacao"] = edificacao

    qs = models.PontoColeta.objects.create(**data_dict)

    return qs

@router.put("/{id_ponto}")
def update_ponto(request, id_ponto: int, payload: PontoColetaIn):
    ponto = get_object_or_404(models.PontoColeta, id=id_ponto)
    for attr, value in payload.dict().items():
        setattr(ponto, attr, value)
    ponto.save()
    return {"success": True}

@router.delete("/pontos/{id_ponto}")
def delete_ponto(request, id_ponto: int):
    ponto = get_object_or_404(models.PontoColeta, id=id_ponto)
    ponto.delete()
    return {"success": True}

# https://django-ninja.rest-framework.com/tutorial/other/crud/
# https://django-ninja.rest-framework.com/guides/response/?h=resolvers#resolvers