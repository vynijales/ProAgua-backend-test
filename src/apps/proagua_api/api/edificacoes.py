from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from .schemas.edficacao import *
from .schemas.ponto_coleta import (PontoColetaIn, PontoColetaOut)
from .. import models

router = Router()

@router.get("/", response=List[EdificacaoOut], tags=["Edificacoes"])
@paginate
def list_edificacoes(request):
    qs = models.Edificacao.objects.all()
    return qs

@router.get("/{cod_edificacao}", response=EdificacaoOut, tags=["Edificacoes"])
def get_edificacao(request, cod_edificacao: str):
    qs = get_object_or_404(models.Edificacao, codigo=cod_edificacao)
    return qs

@router.post("/", tags=["Edificacoes"])
def create_edificacao(request, payload: EdificacaoIn):
    edificacao = models.Edificacao.objects.create(**payload.dict())
    edificacao.save()
    return {"success": True}

@router.put("/{cod_edificacao}", tags=["Edificacoes"])
def update_edificacoes(request, cod_edificacao: str, payload: EdificacaoIn):
    edificacao = get_object_or_404(models.Edificacao, codigo=cod_edificacao)
    for attr, value in payload.dict().items():
        setattr(edificacao, attr, value)
    edificacao.save()
    return {"success": True}

@router.delete("/{cod_edificacao}", tags=["Edificacoes"])
def delete_edificacao(request, cod_edificacao: str):
    edificacao = get_object_or_404(models.Edificacao, codigo=cod_edificacao)
    edificacao.delete()
    return {"success": True}

@router.get("/{cod_edificacao}/pontos", response=List[PontoColetaOut], tags=["Edificacoes"])
def list_pontos(request, cod_edificacao: str):
    qs = models.PontoColeta.objects.filter(edificacao__codigo=cod_edificacao)
    return qs
