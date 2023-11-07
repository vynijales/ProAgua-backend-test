from typing import List, Optional
from datetime import date

from ninja import Schema, FilterSchema, Field
from django.urls import reverse

from ... import models

class ColetaIn(Schema):
    sequencia_id: int
    ponto_id: int
    temperatura: float
    cloro_residual_livre: float
    turbidez: float
    coliformes_totais: bool
    escherichia: bool
    cor: float
    data: date
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
    data: date
    responsavel: List[int]
    ordem: str
    links: dict = {}
    sequencia_url: str
    ponto_url: str

    @staticmethod
    def resolve_sequencia_url(self):
        return reverse("api-1.0.0:get_sequencia", kwargs={"id_sequencia": self.sequencia.id})

    @staticmethod
    def resolve_ponto_url(self):
        return reverse("api-1.0.0:get_ponto", kwargs={"id_ponto": self.ponto.id})

    @staticmethod
    def resolve_links(obj: models.PontoColeta):
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
    def resolve_responsavel(obj: models.Coleta):
        return [responsavel.id for responsavel in obj.responsavel.all()]


class FilterColeta(FilterSchema):
    q: Optional[str] = Field(q=["responsavel__username__contains"])
    data__gte: Optional[date]
    data__lte: Optional[date]
    