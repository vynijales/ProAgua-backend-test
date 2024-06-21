"""
Material de referência:
    https://django-ninja.rest-framework.com/tutorial/other/crud/
    https://django-ninja.rest-framework.com/guides/response/?h=resolvers#resolvers
"""

from typing import List
import uuid

from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Router, Query, UploadedFile, File, Form
from ninja.pagination import paginate
from ninja.errors import HttpError

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
            Q(ambiente__contains=filters.q) | Q(edificacao__nome__contains=filters.q) | Q(edificacao__codigo__contains=filters.q))
        
    if filters.edificacao__campus:
        qs = qs.filter(edificacao__campus=filters.edificacao__campus)

    if filters.tipo:
        qs = qs.filter(tipo__in=filters.tipo)

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
def upload_image(request, id_ponto: str, description: str = Form(...), file: UploadedFile = File(...)):
    ponto = get_object_or_404(models.PontoColeta, id=id_ponto)

    img_path = save_file(f'media/images/pontos/ponto_{ponto.id}_{uuid.uuid4()}.png', file)
    image = models.Image.objects.create(src=img_path, description=description)
    image.save()

    ponto.imagens.add(image)
    ponto.save()
    
    return {"success": True}


@router.delete('/{id_ponto}/imagem/{id_imagem}')
def delete_image(request, id_ponto: str, id_imagem: uuid.UUID):
    ponto = get_object_or_404(models.PontoColeta, id=id_ponto)
    image: models.Image = ponto.imagens.filter(id=id_imagem).first()
    
    if image is None:
        return HttpError(404, "Not found")
    
    image.src.delete()
    image.delete()
    return {"success": True}


@router.post("/")
def create_ponto(request, payload: PontoColetaIn):
    edificacao = get_object_or_404(models.Edificacao, codigo=payload.codigo_edificacao)
    amontante = get_object_or_404(models.PontoColeta, id=payload.amontante) if payload.amontante else None
    associados = [get_object_or_404(models.PontoColeta, id=assoc) for assoc in payload.associados] if payload.associados else None
    
    data_dict = payload.dict()
    data_dict.pop("codigo_edificacao")
    data_dict.pop("associados", None)
    data_dict["edificacao"] = edificacao
    data_dict["amontante"] = amontante
    ponto_coleta = models.PontoColeta.objects.create(**data_dict)
    
    if associados:
        ponto_coleta.associados.set(associados)

    ponto_coleta.save()

    return {
        "id": ponto_coleta.id,
        "success": True
    }

@router.put("/{id_ponto}")
def update_ponto(request, id_ponto: int, payload: PontoColetaIn):
    ponto = get_object_or_404(models.PontoColeta, id=id_ponto)

    amontante = None
    if payload.amontante is not None:
        amontante = get_object_or_404(models.PontoColeta, id=payload.amontante)

    associados = [get_object_or_404(models.PontoColeta, id=assoc) for assoc in payload.associados] if payload.associados else None

    edificacao = get_object_or_404(models.Edificacao, codigo=payload.codigo_edificacao)

    data_dict = payload.dict()
    data_dict.pop("codigo_edificacao")
    data_dict["edificacao"] = edificacao
    data_dict["amontante"] = amontante

    for attr, value in data_dict.items():
        if attr == "associados":
            ponto.associados.set(value)
        else:
            setattr(ponto, attr, value)
    ponto.save()
    return {"success": True}


@router.delete("/{id_ponto}")
def delete_ponto(request, id_ponto: int):
    ponto = get_object_or_404(models.PontoColeta, id=id_ponto)

    if models.PontoColeta.has_dependent_objects(ponto):
        raise HttpError(409, "Conflict: Related objects exist")
    
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
