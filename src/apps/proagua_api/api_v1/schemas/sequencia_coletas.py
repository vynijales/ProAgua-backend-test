from ninja import Schema


class SequenciaColetasIn(Schema):
    id: int
    amostragem: int


class SequenciaColetasOut(Schema):
    id: int
    amostragem: int
