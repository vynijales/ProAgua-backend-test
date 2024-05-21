from typing import Optional, List

from ninja import Schema
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

    @staticmethod
    def resolve_coletas(obj: SequenciaColetas):
        return Coleta.objects.filter(sequencia=obj.id).order_by("data")

    @staticmethod
    def resolve_coletas_url(obj):
        return reverse("api-1.0.0:list_coletas_sequencia", kwargs={"id_sequencia": obj.id})

    @staticmethod
    def resolve_status(obj) -> Optional[bool]:
        if obj.coletas.last():
            print("Status: ", obj.coletas.last().analise()["status"])
            return obj.coletas.last().analise()["status"]

    @staticmethod
    def resolve_status_message(obj: SequenciaColetas):
        messages = []
        if obj.coletas.last():
            messages.extend(obj.coletas.last().analise()["messages"])
            return ', '.join(messages) + "."
        return "Coleta pendente."