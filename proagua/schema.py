from ninja import Schema
from datetime import date
from typing import List

# SchemasIn

class EdificacaoIn(Schema):
    codigo: str
    nome: str
    campus: str

class PontoColetaIn(Schema):
    edificacao: EdificacaoIn
    ambiente: str
    tipo: str
    mes: int
    pai: int

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
    edificacao: EdificacaoIn
    ambiente: str
    tipo: str
    mes: int
    pai: int


