from typing import List
from datetime import date

from ninja import Schema
from django.urls import reverse


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
    data: date
    responsavel: List[int]
    ordem: str


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
    data: date
    responsavel: List[int]
    ordem: str

    @staticmethod
    def resolve_ponto(obj):
        return reverse("api-1.0.0:get_ponto", kwargs={"id":obj.ponto_coleta.id})
