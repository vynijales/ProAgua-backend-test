from datetime import date
from typing import List

from django.urls import reverse
from ninja import Schema

# SchemasIn

class EdificacaoIn(Schema):
    codigo: str
    nome: str
    campus: str 
    cronograma: int

class PontoColetaIn(Schema):
    id: int 
    edificacao_codigo: str
    ambiente: str
    tipo: int
    amontante_id: int = None

class ColetaIn(Schema):
    id: int
    sequencia_id: int
    ponto_id: int
    temperatura: float
    cloro_residual_livre: float
    turbidez: float
    coliformes_totais: bool
    escherichia: bool
    cor: float
    date: date
    responsavel: List[int]
    ordem: str

class SequenciaColetasIn(Schema):
    id: int
    amostragem: int

# SchemasOut

class EdificacaoOut(Schema):
    codigo: str
    nome: str
    campus: str 
    cronograma: int

class PontoColetaOut(Schema):
    id: int 
    edificacao_codigo: str = None
    ambiente: str
    tipo: int
    amontante_id: int = None

    @staticmethod
    def resolve_edificacao(obj):
        return reverse("api-1.0.0:get_edificacao", kwargs={"cod_edificacao":obj.edificacao.codigo})

class ColetaOut(Schema):
    id: int
    sequencia_id: int
    ponto_id: int
    temperatura: float
    cloro_residual_livre: float
    turbidez: float
    coliformes_totais: bool
    escherichia: bool
    cor: float
    date: date
    responsavel: List[int]
    ordem: str

    @staticmethod
    def resolve_ponto(obj):
        return reverse("api-1.0.0:get_ponto", kwargs={"id":obj.ponto_coleta.id})

class SequenciaColetasOut(Schema):
    id: int
    amostragem: int