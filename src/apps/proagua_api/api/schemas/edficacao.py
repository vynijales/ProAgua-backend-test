from typing import Optional, List
import os

from ninja import Schema, FilterSchema, Field, UploadedFile
from django.urls import reverse_lazy
from django.conf import settings
from apps.proagua_api import models
from .image import ImageOut, ImageIn

class EdificacaoIn(Schema):
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
    imagens: List[ImageOut]
    
    @staticmethod
    def resolve_pontos_url(obj):
        return str(reverse_lazy("api-1.0.0:list_pontos", kwargs={"cod_edificacao": obj.codigo}))
    


class FilterEdificacao(FilterSchema):
    q: Optional[str] = Field(q=['nome__contains', 'codigo__contains'])
    cronograma__gte: Optional[int]
    cronograma__lte: Optional[int]
    campus: Optional[str]
