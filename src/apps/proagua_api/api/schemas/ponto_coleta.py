from ninja import Schema
from django.urls import reverse


class PontoColetaIn(Schema):
    id: int 
    edificacao_codigo: str
    ambiente: str
    tipo: int
    amontante_id: int = None


class PontoColetaOut(Schema):
    id: int 
    edificacao_codigo: str = None
    ambiente: str
    tipo: int
    amontante_id: int = None

    @staticmethod
    def resolve_edificacao(obj):
        return reverse("api-1.0.0:get_edificacao", kwargs={"cod_edificacao":obj.edificacao.codigo})
