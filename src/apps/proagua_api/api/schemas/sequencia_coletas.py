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
    ponto_url: Optional[str]
    coletas: List[ColetaOut]

    @staticmethod
    def resolve_ponto_url(obj):
        pontos = PontoColeta.objects.filter(coletas__sequencia=obj.id)
        ponto = pontos.order_by('tipo').first()
        
        if ponto:
            return reverse("api-1.0.0:get_ponto", kwargs={"id_ponto": ponto.id})
        
        return None
