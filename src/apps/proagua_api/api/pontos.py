"""
Material de referência:
    https://django-ninja.rest-framework.com/tutorial/other/crud/
    https://django-ninja.rest-framework.com/guides/response/?h=resolvers#resolvers
"""

from typing import List

from django.db.models import Q, Subquery, OuterRef
from django.shortcuts import get_object_or_404
from ninja import Router, Query, UploadedFile, File
from ninja.pagination import paginate

from .schemas.ponto_coleta import *
from .schemas.coleta import ColetaOut
from .schemas.fluxo import FluxoOut
from .. import models
from .utils import save_file

router = Router(tags=["Pontos"])

@router.get("/", response=List[PontoColetaOut])
@paginate
def list_ponto(request, filters: FilterPontos = Query(...)):
    qs = models.PontoColeta.objects

    if filters.q:
        qs = qs.filter(
            Q(ambiente__contains=filters.q) | Q(edificacao__nome__contains=filters.q)
        )
        
    if filters.edificacao__campus:
        qs = qs.filter(edificacao__campus=filters.edificacao__campus)

    if filters.tipo:
        qs = qs.filter(tipo=filters.tipo)

    if filters.fluxos:
        qs = qs.filter(fluxos=filters.fluxos)

    if filters.status:
        pass

    return qs.all()


@router.get("/{id_ponto}", response=PontoColetaOut)
def get_ponto(request, id_ponto: int):
    qs = get_object_or_404(models.PontoColeta, id=id_ponto)
    return qs


@router.post("/{id_ponto}/imagem")
def upload_image(request, id_ponto: str, imagem: UploadedFile = File(...)):
    ponto = get_object_or_404(models.PontoColeta, id=id_ponto)

    im_path = save_file(f'media/images/pontos/ponto_{ponto.id}.png', imagem)
    ponto.imagem = im_path
    ponto.save()
    
    return {"success": True}


@router.post("/")
def create_ponto(request, payload: PontoColetaIn):
    edificacao = get_object_or_404(models.Edificacao, codigo=payload.codigo_edificacao)

    data_dict = payload.dict()
    data_dict.pop("codigo_edificacao")
    data_dict["edificacao"] = edificacao

    ponto_coleta = models.PontoColeta.objects.create(**data_dict)
    ponto_coleta.save()

    return {
        "id": ponto_coleta.id,
        "success": True
        }


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
