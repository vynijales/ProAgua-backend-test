from typing import Optional
import os

from ninja import Schema, FilterSchema, Field, UploadedFile
from django.urls import reverse_lazy
from django.conf import settings
from apps.proagua_api import models

class EdificacaoIn(Schema):
    imagem: Optional[str]
    codigo: str
    nome: str
    campus: str 
    cronograma: int


class EdificacaoOut(Schema):
    imagem: Optional[str]
    codigo: str
    nome: str
    campus: str 
    cronograma: int
    pontos_url: str
    
    @staticmethod
    def resolve_pontos_url(obj):
        return str(reverse_lazy("api-1.0.0:list_pontos", kwargs={"cod_edificacao": obj.codigo}))

    @staticmethod
    def resolve_imagem(obj: models.Edificacao):
        if obj.imagem:
            img_path = os.path.relpath(obj.imagem.path, settings.MEDIA_ROOT)
            return os.path.join(settings.MEDIA_URL, img_path)


class FilterEdificacao(FilterSchema):
    q: Optional[str] = Field(q=['nome__contains', 'codigo__contains'])
    cronograma__gte: Optional[int]
    cronograma__lte: Optional[int]
    campus: Optional[str]
