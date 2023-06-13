from django.forms import ModelForm
from . import models

class CreatePontoColeta(ModelForm):
    class Meta:
        model = models.PontoColeta
        fields = ["edificacao", "ambiente", "tipo", "mes", "pai"]

class CreateColeta(ModelForm):
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