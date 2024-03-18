from typing import Optional, List

from ninja import Schema
from django.urls import reverse

from apps.proagua_api.models import PontoColeta
from .coleta import ColetaOut

class SequenciaColetasIn(Schema):
    amostragem: int


class SequenciaColetasOut(Schema):
    id: int
    amostragem: int
    ponto: Optional[PontoColetaOut]
    coletas: List[ColetaOut]

    @staticmethod
    def resolve_ponto(obj):
        pontos = PontoColeta.objects.filter(coletas__sequencia=obj.id)
        return pontos.order_by('tipo').first()

