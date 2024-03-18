from typing import Optional

from ninja import Schema, FilterSchema, Field
from django.urls import reverse
from .edficacao import EdificacaoOut

class PontoColetaIn(Schema):
    codigo_edificacao: str
    ambiente: str
    tombo: Optional[str]
    tipo: int


class PontoColetaOut(Schema):
    id: int
    imagem: Optional[str]
    ambiente: str
    tipo: int
    tombo: Optional[str]
    edificacao: EdificacaoOut
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
    edificacao__campus: Optional[str] = Field(alias="campus")
    tipo: Optional[int]
    fluxos: Optional[int]
