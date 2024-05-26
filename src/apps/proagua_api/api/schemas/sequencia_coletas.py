from typing import Optional, List
from datetime import date, datetime

from ninja import Field, FilterSchema, Schema
from django.urls import reverse

from .coleta import ColetaOut
from .ponto_coleta import PontoColetaOut

from ...models import SequenciaColetas, Coleta, PontoColeta


class SequenciaColetasIn(Schema):
    amostragem: int
    ponto: int


class SequenciaColetasOut(Schema):
    id: int
    amostragem: int
    ponto: PontoColetaOut
    coletas: List[ColetaOut]
    coletas_url: str
    status: Optional[bool]
    status_message: Optional[str]
    ultima_coleta: Optional[datetime]

    @staticmethod
    def resolve_coletas(obj: SequenciaColetas):
        return Coleta.objects.filter(sequencia=obj.id).order_by("data")

    @staticmethod
    def resolve_coletas_url(obj):
        return reverse("api-1.0.0:list_coletas_sequencia", kwargs={"id_sequencia": obj.id})

    @staticmethod
    def resolve_status(obj) -> Optional[bool]:
        if obj.coletas.last():
            return obj.coletas.last().analise()["status"]

    @staticmethod
    def resolve_status_message(obj: SequenciaColetas):
        messages = []
        if obj.coletas.last():
            messages.extend(obj.coletas.last().analise()["messages"])
            return ', '.join(messages) + "."
        return "Coleta pendente."

    @staticmethod
    def resolve_ultima_coleta(obj: SequenciaColetas):
        if obj.coletas.order_by("data").last():
            return obj.coletas.last().data
        return None


class FilterSequenciaColetas(FilterSchema):

    q: Optional[str] = Field(
        q=["ponto__ambiente__contains", "ponto__edificacao__nome__contains", "ponto__edificacao__codigo__contains"],
        description="Campo de pesquisa por ambiente ou nome de edificação"
    )
    amostragem: Optional[int] = Field(alias="amostragem")
    ponto__id: Optional[int] = Field(alias="ponto_id")
    ponto__edificacao__campus: Optional[str] = Field(alias="campus")
    status: Optional[bool] = Field(alias="status")