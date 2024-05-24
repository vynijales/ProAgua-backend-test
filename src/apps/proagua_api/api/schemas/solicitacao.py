from typing import Optional, List
from datetime import date, datetime

from ninja import Schema, FilterSchema

from .ponto_coleta import PontoColetaOut

class SolicitacaoIn(Schema):
    ponto_id: int
    data: datetime
    status: str
    observacao: Optional[str] = None
    justificativa: Optional[str] = None

class SolicitacaoOut(Schema):
    id: int
    ponto: PontoColetaOut
    data: datetime
    status: str
    observacao: Optional[str] = None
    justificativa: Optional[str] = None

class FilterSolicitacao(FilterSchema):
    ponto_id__exact: Optional[int]
    status__exact: Optional[str]
    data__gte: Optional[date]
    data__lte: Optional[date]
