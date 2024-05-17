from ninja import Schema, Field

from typing import Optional

from ... import models

class ParametrosReferenciaIn(Schema):
    min_temperatura: Optional[float]
    max_temperatura: Optional[float]
    min_cloro_residual_livre: Optional[float]
    max_cloro_residual_livre: Optional[float]
    min_turbidez: Optional[float]
    max_turbidez: Optional[float]
    coliformes_totais: bool
    escherichia: bool

class ParametrosReferenciaOut(Schema):
    min_temperatura: Optional[float]
    max_temperatura: Optional[float]
    min_cloro_residual_livre: Optional[float]
    max_cloro_residual_livre: Optional[float]
    min_turbidez: Optional[float]
    max_turbidez: Optional[float]
    coliformes_totais: Optional[bool]
    escherichia: Optional[bool]

