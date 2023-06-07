from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Edificacao(models.Model):
    codigo = models.CharField(
        verbose_name='código',
        max_length=20,
    )
    nome = models.CharField(
        verbose_name='nome da edificação',
        max_length=80,
    )
    bloco = models.CharField(
        max_length=1,
        verbose_name='bloco',
        choices=(
            ('L', 'leste'),
            ('O', 'oeste')
        ),
        default=('L', 'leste')
    )

    def __str__(self):
        return f'{self.codigo} - {self.nome}'


class PontoColeta(models.Model):
    edificacao = models.ForeignKey(
        to=Edificacao,
        verbose_name='edificação',
        on_delete=models.PROTECT,
    )
    ambiente = models.CharField(
        verbose_name='ambiente',
        max_length=120,
    )
    tipo = models.CharField(
        max_length=2,
        choices=(
            ("BE", "Bebedouro"),
            ("TO", "Torneira"),
            ("RS", "Reservatório superior"),
            ("RI", "Reservatório inferior")
        ),
        default=("BE", "Bebedouro")
    )
    pai = models.ForeignKey(
        to='PontoColeta',
        verbose_name='Ponto de coleta pai',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.edificacao.nome} - {self.ambiente}'


class Coleta(models.Model):
    id = models.AutoField(
        primary_key=True,
        verbose_name="ID",
        editable=False,
    )
    ponto_coleta = models.ForeignKey(
        to=PontoColeta,
        verbose_name='ponto de coleta',
        on_delete=models.PROTECT,
    )
    temperatura = models.FloatField(
        verbose_name="temperatura",
    )
    cloro_residual_livre = models.FloatField(
        verbose_name="cloro residual livre",
    )

    cloro_total = models.FloatField(
        verbose_name="cloro total",
    )

    turbidez = models.FloatField(
        verbose_name="turbidez",
    )

    coliformes_totais = models.BooleanField(
        verbose_name="coliformes totais",
    )

    escherichia = models.BooleanField(
        verbose_name="escherichia",
    )

    cor = models.CharField(
        verbose_name="cor",
        max_length=20,
    )
    date = models.DateTimeField(
        verbose_name="data da coleta",
        # db_comment="Data e hora de quando foi realizada a coleta",
    )
    responsavel = models.ManyToManyField(
        to=User,
        verbose_name="responsáveis",
    )
    ordem = models.CharField(
        max_length=1,
        choices=(
            ("C", "Coleta"),
            ("R", "Recoleta")
        ),
        default=("C", "Coleta"),
    )
    amostragem = models.PositiveIntegerField(
        verbose_name="amostragem",
        default=0,

    )

    def __str__(self):
        return f'ID {self.id}: {self.ordem} - {self.date}'