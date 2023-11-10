from typing import List
import os

from django.shortcuts import get_object_or_404
from django.conf import settings
from ninja import Router, Query, UploadedFile, File, Form
from ninja.pagination import paginate

from .schemas.edficacao import *
from .schemas.ponto_coleta import (PontoColetaIn, PontoColetaOut)
from .. import models

router = Router()

def save_file(file_path: str, file: UploadedFile=File(...)) -> str:
    file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'wb') as destination_file:
        destination_file.write(file.read())

    return os.path.relpath(file_path, settings.MEDIA_ROOT)


@router.get("/", response=List[EdificacaoOut], tags=["Edificacoes"])
@paginate
def list_edificacoes(request, filters: FilterEdificacao = Query(...)):
    qs = models.Edificacao.objects.all()
    return filters.filter(qs)


@router.get("/{cod_edificacao}", response=EdificacaoOut, tags=["Edificacoes"])
def get_edificacao(request, cod_edificacao: str):
    qs = get_object_or_404(models.Edificacao, codigo=cod_edificacao)
    return qs


@router.post("/", response=EdificacaoOut, tags=["Edificacoes"])
def create_edificacao(request, payload: EdificacaoIn = Form(...), imagem: UploadedFile = File(...)):
    im_path = save_file(f'media/images/edificacoes/{imagem.name}', imagem)

    data = payload.dict()
    data['imagem'] = im_path

    edificacao = models.Edificacao.objects.create(**data)
    edificacao.save()
    
    return edificacao


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
