from typing import Optional, List

from ninja import Schema
from django.urls import reverse

from apps.proagua_api.models import PontoColeta
from .coleta import ColetaOut
from .ponto_coleta import PontoColetaOut

class SequenciaColetasIn(Schema):
    amostragem: int
    ponto: int

class SequenciaColetasOut(Schema):
    id: int
    amostragem: int
    ponto: PontoColetaOut
    coletas_url: str

    @staticmethod
    def resolve_coletas_url(obj):
        return reverse("api-1.0.0:list_coletas_sequencia", kwargs={"id_sequencia": obj.id})