from typing import List

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from ninja import Router, Query

from .schemas.coleta import *
from .schemas.usuario import UsuarioOut
from .. import models

router = Router(tags=["Coletas"])


@router.get("/", response=List[ColetaOut])
def list_coleta(request, filter: FilterColeta = Query(...)):
    qs = models.Coleta.objects.all()
    return filter.filter(qs)


@router.get("/{id_coleta}", response=ColetaOut)
def get_coleta(request, id_coleta: int):
    qs = get_object_or_404(models.Coleta, id=id_coleta)
    return qs


@router.post("/")
def create_coleta(request, payload: ColetaIn):
    data_dict = payload.dict()
    responsavel_ids = data_dict.get("responsavel", [])

    # Removendo a lista de responsáveis do dicionário para criar a instância da Coleta
    del data_dict["responsavel"]

    obj_seq = get_object_or_404(
        models.SequenciaColetas, id=data_dict.get("sequencia_id"))

    # Criando a instância da Coleta sem os responsáveis
    obj_coleta = models.Coleta.objects.create(**data_dict, sequencia=obj_seq)

    # Use o método set para adicionar os responsáveis após a criação
    for responsavel_id in responsavel_ids:
        user = User.objects.filter(id=responsavel_id).first()
        if user:
            obj_coleta.responsavel.add(user)

    return {"success": True}


@router.put("/{id_coleta}")
def update_coleta(request, id_coleta: int, payload: ColetaIn):
    obj_coleta = get_object_or_404(models.Coleta, id=id_coleta)
    data_dict = payload.dict()
    responsavel_ids = data_dict.get("responsavel", [])

    # Removendo a lista de responsáveis do dicionário
    del data_dict["responsavel"]

    # Iterando sobre os campos no payload e atualizar os valores correspondentes na instância
    for attr, value in data_dict.items():
        setattr(obj_coleta, attr, value)

    # Atualizando os responsáveis
    obj_coleta.responsavel.clear()
    for responsavel_id in responsavel_ids:
        user = User.objects.filter(id=responsavel_id).first()
        if user:
            obj_coleta.responsavel.add(user)

    obj_coleta.save()

    return {"success": True}


@router.delete("/{id_coleta}")
def delete_coleta(request, id_coleta: int):
    obj_coleta = get_object_or_404(models.Coleta, id=id_coleta)
    obj_coleta.delete()
    return {"success": True}


@router.get("/{id_coleta}/responsaveis", response=List[UsuarioOut])
def get_responsaveis_coleta(request, id_coleta: int):
    coleta = get_object_or_404(models.Coleta, id=id_coleta)
    return coleta.responsavel
