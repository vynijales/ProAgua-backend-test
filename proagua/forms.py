from django import forms
from . import models
import datetime

class FormPontoColeta(forms.ModelForm):
    class Meta:
        model = models.PontoColeta
        fields = ["edificacao", "ambiente", "tipo", "mes", "pai"]

class FormColeta(forms.ModelForm):
    class Meta:
        model = models.Coleta
        fields = [
            "ponto_coleta",
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
            "amostragem",
            "fluxo",
        ]

class FormEdificacao(forms.ModelForm):
    class Meta:
        model = models.Edificacao
        fields = ['codigo', 'nome', 'bloco']

class FormSearchPontos(forms.Form):
    bloco = forms.ChoiceField(choices=[('L', "Leste"), ("O", "Oeste")], required=False)
    tipo = forms.MultipleChoiceField(
        choices=(
            ("BE", "Bebedouro"),
            ("TO", "Torneira"),
            ("RS", "Reservatório superior"),
            ("RI", "Reservatório inferior")
        ),
        required= False,
        widget=forms.CheckboxSelectMultiple,
        initial=(
            ("BE", "Bebedouro"),
            ("TO", "Torneira"),
        )
    )

    data_minima = forms.DateField(label="Data Mínima", widget=forms.SelectDateWidget(years=range(2010, datetime.datetime.now().year + 1)), required=False, initial=(1,0,2000))
    data_maxima = forms.DateField(label="Data Máxima", widget=forms.SelectDateWidget(years=range(2010, datetime.datetime.now().year + 1)), required=False)

