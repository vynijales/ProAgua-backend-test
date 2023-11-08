from typing import Optional
from ninja import Schema, FilterSchema, Field
from django.urls import reverse_lazy

class EdificacaoIn(Schema):
    codigo: str
    nome: str
    campus: str 
    cronograma: int


class EdificacaoOut(Schema):
    codigo: str
    nome: str
    campus: str 
    cronograma: int
    pontos_url: str
    
    @staticmethod
    def resolve_pontos_url(self):
        return str(reverse_lazy("api-1.0.0:list_pontos", kwargs={"cod_edificacao": self.codigo}))


class FilterEdificacao(FilterSchema):
    q: Optional[str] = Field(q=['nome__contains', 'codigo__contains'])
    cronograma__gte: Optional[int]
    cronograma__lte: Optional[int]
    campus: Optional[str]
