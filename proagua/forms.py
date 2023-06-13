from django.forms import ModelForm
from . import models

class FormPontoColeta(ModelForm):
    class Meta:
        model = models.PontoColeta
        fields = ["edificacao", "ambiente", "tipo", "mes", "pai"]

class FormColeta(ModelForm):
    class Meta:
        model = models.Coleta
        fields = [
            "temperatura",
            "cloro_residual_livre",
            "cloro_total",
            "turbidez",
            "coliformes_totais",
            "escherichia",
            "cor",
            "date",
            "responsavel",
            "ordem",
            "amostragem"
        ]

class FormEdificacao(ModelForm):
    class Meta:
        model = models.Edificacao
        fields = ['codigo', 'nome', 'bloco']