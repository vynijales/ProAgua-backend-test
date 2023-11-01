"""
Material de referência:
    https://django-ninja.rest-framework.com/tutorial/other/crud/
    https://django-ninja.rest-framework.com/guides/response/?h=resolvers#resolvers
"""

from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from .schemas.ponto_coleta import *
from .schemas.coleta import ColetaOut
from .schemas.fluxo import FluxoOut
from .. import models

router = Router()

@router.get("/", response=List[PontoColetaOut])
@paginate
def list_ponto(request):
    qs = models.PontoColeta.objects.all()
    return qs

@router.get("/{id_ponto}", response=PontoColetaOut)
def get_ponto(request, id_ponto: int):
    qs = get_object_or_404(models.PontoColeta, id=id_ponto)
    return qs

@router.post("/")
def create_ponto(request, payload: PontoColetaIn):
    edificacao = get_object_or_404(models.Edificacao, codigo=payload.codigo_edificacao)

    data_dict = payload.dict()
    data_dict.pop("codigo_edificacao")
    data_dict["edificacao"] = edificacao

    qs = models.PontoColeta.objects.create(**data_dict)

    return {"success": True}

@router.put("/{id_ponto}")
def update_ponto(request, id_ponto: int, payload: PontoColetaIn):
    ponto = get_object_or_404(models.PontoColeta, id=id_ponto)
    for attr, value in payload.dict().items():
        setattr(ponto, attr, value)
    ponto.save()
    return {"success": True}

@router.delete("/{id_ponto}")
def delete_ponto(request, id_ponto: int):
    ponto = get_object_or_404(models.PontoColeta, id=id_ponto)
    ponto.delete()
    return {"success": True}

@router.get("/{id_ponto}/coletas", response=List[ColetaOut])
def list_coletas(request, id_ponto: int):
    """
    Retorna todas as coletas associadas a um ponto de coleta
    """
    qs = models.Coleta.objects.filter(ponto__id=id_ponto)
    return qs

@router.get("/{id_ponto}/fluxos", response=List[FluxoOut])
def get_fluxos(request, id_ponto: int):
    fluxos = models.Fluxo.objects.filter(pontos__id=id_ponto)
    return fluxos
