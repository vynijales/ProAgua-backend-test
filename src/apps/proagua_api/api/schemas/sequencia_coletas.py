from ninja import Schema


class SequenciaColetasIn(Schema):
    amostragem: int


class SequenciaColetasOut(Schema):
    id: int
    amostragem: int
