from datetime import date
from typing import List

from django.urls import reverse
from ninja import Schema

# SchemasIn

class EdificacaoIn(Schema):
    codigo: str
    nome: str
    campus: str

class PontoColetaIn(Schema):
    edificacao_codigo: str = None
    ambiente: str
    tipo: str
    mes: int
    # pai: int = None

class ColetaIn(Schema):
    id: int
    ponto_coleta: PontoColetaIn
    temperatura: float
    cloro_residual_livre: float
    turbidez: float
    coliformes_totais: bool
    escherichia: bool
    cor: float
    date: date
    responsavel: List[int]
    ordem: str
    amostragem: int
    fluxo: int
    
# SchemasOut

class EdificacaoOut(Schema):
    codigo: str
    nome: str
    campus: str

class PontoColetaOut(Schema):
    id: int
    edificacao: str
    ambiente: str
    tipo: str
    mes: int
    # pai: int

    @staticmethod
    def resolve_edificacao(obj):
        return reverse("api-1.0.0:get_edificacao", kwargs={"cod_edificacao":obj.edificacao.codigo})
