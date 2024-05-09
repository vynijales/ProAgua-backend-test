from typing import Optional, ForwardRef

from ninja import Schema, FilterSchema, Field
from django.urls import reverse
from .edficacao import EdificacaoOut
from ... import models

PontoColetaInRef = ForwardRef('PontoColetaIn')
PontoColetaOutRef = ForwardRef('PontoColetaOut')

class PontoColetaIn(Schema):
    codigo_edificacao: str
    ambiente: str
    tombo: Optional[str]
    tipo: int
    amontante: Optional[int]


class PontoColetaOut(Schema):
    id: int
    imagem: Optional[str]
    ambiente: str
    tipo: int
    tombo: Optional[str]
    edificacao: EdificacaoOut
    edificacao_url: str
    fluxos_url: str
    status: Optional[bool]
    status_message: Optional[str]
    amontante: Optional[PontoColetaOutRef] # type: ignore

    @staticmethod
    def resolve_edificacao_url(self):
        return reverse("api-1.0.0:get_edificacao", kwargs={"cod_edificacao": self.edificacao.codigo})

    @staticmethod
    def resolve_fluxos_url(self):
        return reverse("api-1.0.0:get_fluxos", kwargs={"id_ponto": self.id})
    
    @staticmethod
    def resolve_status_message(obj: models.PontoColeta):
        messages = []
        for coleta in obj.coletas.all():
            messages.extend(coleta.analise()["messages"])

        if len(messages) > 0:
            return ', '.join(messages)
        
        return "Não há coletas nesse ponto"

class FilterPontos(FilterSchema):
    q: Optional[str] = Field(
        q=["ambiente__contains", "edificacao__nome__contains"],
        description="Campo de pesquisa por ambiente ou nome de edificação"
    )
    edificacao__campus: Optional[str] = Field(alias="campus")
    tipo: Optional[int]
    fluxos: Optional[int]
    # status: Optional[bool]
    status: Optional[bool] = Field("coletas__last")


PontoColetaIn.update_forward_refs()
PontoColetaOut.update_forward_refs()