from typing import Optional

from ninja import Schema, FilterSchema, Field
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
    
    # Substituir amontante_id por amontante_url ?
    amontante_id: int = None 
    
    edificacao_url: str
    fluxos_url: str
    

    @staticmethod
    def resolve_edificacao_url(self):
        return reverse("api-1.0.0:get_edificacao", kwargs={"cod_edificacao": self.edificacao.codigo})

    @staticmethod
    def resolve_fluxos_url(self):
        return reverse("api-1.0.0:get_fluxos", kwargs={"id_ponto": self.id})

class FilterPontos(FilterSchema):
    q: Optional[str] = Field(
        q=["ambiente__contains", "edificacao__nome__contains"],
        description="Campo de pesquisa por ambiente ou nome de edificação"
    )
    tipo: Optional[int]
    amontante_id: Optional[int]
    fluxos: Optional[int]
