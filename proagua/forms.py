from django import forms
from . import models
import datetime

class FormPontoColeta(forms.ModelForm):
    class Meta:
        model = models.PontoColeta
        fields = ["edificacao", "ambiente", "tipo", "amontante"]

class FormColeta(forms.ModelForm):
    class Meta:
        model = models.Coleta
        fields = [
            # "ponto_coleta",
            "temperatura",
            "cloro_residual_livre",
            "turbidez",
            "coliformes_totais",
            "escherichia",
            "cor",
            "data",
            "responsavel",
            "ordem",
        ]

class FormEdificacao(forms.ModelForm):
    class Meta:
        model = models.Edificacao
        fields = ['codigo', 'nome', 'campus', 'cronograma']

class FormSearchPontos(forms.Form):
    campus = forms.ChoiceField(choices=[('', '---'), ('L', "Leste"), ("O", "Oeste")], required=False)
    tipo = forms.MultipleChoiceField(
        choices=(
            ("BE", "Bebedouro"),
            ("RS", "Reservatório superior"),
            ("RI", "Reservatório inferior")
        ),
        required= False,
        widget=forms.CheckboxSelectMultiple,
    )

    data_minima = forms.DateField(label="Data Mínima", widget=forms.SelectDateWidget(years=range(2010, datetime.datetime.now().year + 1)), required=False, initial=(1,0,2000))
    data_maxima = forms.DateField(label="Data Máxima", widget=forms.SelectDateWidget(years=range(2010, datetime.datetime.now().year + 1)), required=False)

