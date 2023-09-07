from ninja import Schema

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
