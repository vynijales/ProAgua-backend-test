from typing import List, Optional
from datetime import date, datetime

from ninja import Schema, FilterSchema, Field
from django.urls import reverse

from ... import models
from .ponto_coleta import PontoColetaOut

class ColetaIn(Schema):
    sequencia_id: int
    ponto_id: int
    temperatura: float
    cloro_residual_livre: float
    turbidez: float
    coliformes_totais: bool
    escherichia: bool
    cor: float
    data: datetime
    responsavel: List[int]
    ordem: str


class ColetaOut(Schema):
    id: int
    temperatura: float
    cloro_residual_livre: float
    turbidez: float
    coliformes_totais: bool
    escherichia: bool
    cor: float
    data: datetime
    responsaveis_id: List[int]
    responsaveis_url: str
    ordem: str
    links: dict = {}
    sequencia_url: str
    sequencia_id: int
    ponto_url: str
    ponto: PontoColetaOut
    status: Optional[bool]
    status_messages: Optional[List[str]]

    @staticmethod
    def resolve_responsaveis_id(obj: models.Coleta):
        return [r.id for r in obj.responsavel.all()]

    @staticmethod
    def resolve_responsaveis_url(obj):
        return reverse("api-1.0.0:get_responsaveis_coleta", kwargs={"id_coleta": obj.id})

    @staticmethod
    def resolve_sequencia_url(obj):
        return reverse("api-1.0.0:get_sequencia", kwargs={"id_sequencia": obj.sequencia.id})

    @staticmethod
    def resolve_ponto_url(obj):
        return reverse("api-1.0.0:get_ponto", kwargs={"id_ponto": obj.ponto.id})

    @staticmethod
    def resolve_links(obj: models.Coleta):
        return {
            "sequencia": {
                "id_sequencia": obj.sequencia.id,
                "url_sequencia": reverse("api-1.0.0:get_sequencia", kwargs={"id_sequencia":obj.sequencia.id}),
            }
            ,"ponto_coleta": {
                "id_ponto": obj.ponto.id,
                "url_ponto": reverse("api-1.0.0:get_ponto", kwargs={"id_ponto":obj.ponto.id}),
             }
        }

    @staticmethod
    def resolve_status_messages(obj: models.Coleta):
        return obj.analise()["messages"]

class FilterColeta(FilterSchema):
    responsavel__username__contains: Optional[str] = Field(q=["responsavel__username__contains"])
    data__gte: Optional[date] = Field(alias="data_minima")
    data__lte: Optional[date] = Field(alias="data_maxima")
    sequencia_id: Optional[int] = Field(alias="sequencia__id")
    temperatura__gte: Optional[float] = Field(alias="temperatura_minima")
    temperatura__lte: Optional[float] = Field(alias="temperatura_maxima")
    cloro_residual_livre__gte: Optional[float] = Field(alias="cloro_residual_livre_minimo")
    cloro_residual_livre__lte: Optional[float] = Field(alias="cloro_residual_livre_maximo")
    turbidez__gte: Optional[float] = Field(alias="turbidez_minima")
    turbidez__lte: Optional[float] = Field(alias="turbidez_maxima")
    coliformes_totais: Optional[bool] = Field(alias="coliformes_totais")
    escherichia: Optional[bool] = Field(alias="escherichia")
    cor__gte: Optional[float] = Field(alias="cor_minima")
    cor__lte: Optional[float] = Field(alias="cor_maxima")
    ordem: Optional[str] = Field(alias="ordem")
    ponto__edificacao__codigo__exact: Optional[str] = Field(alias="codigo_edificacao")
    ponto__id: Optional[int] = Field(alias="ponto_id")