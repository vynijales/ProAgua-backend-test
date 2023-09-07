from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router

from .schemas.coleta import *
from .. import models

router = Router()

@router.get("/", response=List[ColetaOut])
def list_coleta(request):
    qs = models.Coleta.objects.all()
    return qs

@router.get("/{id_coleta}", response=ColetaOut)
def get_coleta(request, id_coleta: int):
    qs = get_object_or_404(models.Coleta, id=id_coleta)
    return qs

@router.post("/")
def create_coleta(request, payload: ColetaIn):
    coleta = models.Coleta.objects.create(**payload.dict())
    return {"success": True}

@router.put("/{id_coleta}")
def update_coleta(request, id_coleta: int, payload: ColetaIn):
    coleta = get_object_or_404(models.Coleta, id=id_coleta)
    for attr, value in payload.dict().items():
        setattr(coleta, attr, value)
    coleta.save()
    return {"success": True}

@router.delete("/{id_coleta}")
def delete_coleta(request, id_coleta: int):
    coleta = get_object_or_404(models.Edificacao, id=id_coleta)
    coleta.delete()
    return {"success": True}