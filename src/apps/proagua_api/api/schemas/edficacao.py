from ninja import Schema
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
