from django.forms import ModelForm
from . import models

class CreatePontoColeta(ModelForm):
    class Meta:
        model = models.PontoColeta
        fields = ["edificacao", "ambiente", "tipo", "mes", "pai"]