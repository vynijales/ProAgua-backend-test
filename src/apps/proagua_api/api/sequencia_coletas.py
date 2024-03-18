from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from .schemas.sequencia_coletas import *
from .. import models

router = Router(tags=["Sequencias"])


@router.get("/", response=List[SequenciaColetasOut])
@paginate
def list_sequencia(request):
    qs = models.SequenciaColetas.objects.all()
    return qs


@router.get("/{id_sequencia}", response=SequenciaColetasOut)
def get_sequencia(request, id_sequencia: int):
    qs = get_object_or_404(models.SequenciaColetas, id=id_sequencia)
    return qs


@router.post("/")
def create_sequencia(request, payload: SequenciaColetasIn):
    sequencia = models.SequenciaColetas.objects.create(**payload.dict())
    sequencia.save()
    return {"success": True}


@router.put("/{id_sequencia}")
def update_sequencia(request, id_sequencia: int, payload: SequenciaColetasIn):
    sequencia = get_object_or_404(models.SequenciaColetas, id=id_sequencia)
    for attr, value in payload.dict().items():
        setattr(sequencia, attr, value)
    sequencia.save()
    return {"success": True}


@router.delete("/{id_sequencia}")
def delete_sequencia(request, id_sequencia: int):
    sequencia = get_object_or_404(models.SequenciaColetas, id=id_sequencia)
    sequencia.delete()
    return {"success": True}