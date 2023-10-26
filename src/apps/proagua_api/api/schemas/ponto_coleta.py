from ninja import Schema
from django.urls import reverse

from ... import models

class PontoColetaIn(Schema):
    codigo_edificacao: str
    ambiente: str
    tipo: int
    amontante_id: int = None


class PontoColetaOut(Schema):
    id: int 
    ambiente: str
    tipo: int
    amontante_id: int = None
    links: dict = {}

    @staticmethod
    def resolve_links(obj: models.PontoColeta):
        return {
            "edificacao": { 
                "codigo_edificacao": obj.edificacao.codigo,
                "url_edificacao": reverse("api-1.0.0:get_edificacao", kwargs={"cod_edificacao":obj.edificacao.codigo})
            }
        }