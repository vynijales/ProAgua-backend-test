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

    def __str__(self):
        return f'{self.codigo} - {self.nome}'

class PontoColeta(models.Model):
    edificacao = models.ForeignKey(
        to=Edificacao,
        verbose_name='edificação',
        on_delete=models.CASCADE,
    )
    ambiente = models.CharField(
        verbose_name='ambiente',
        max_length=120,
    )
    torneira = models.BooleanField(
        verbose_name='torneira',
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
        on_delete=models.CASCADE,
    )

    date = models.DateTimeField(
        verbose_name="data da coleta",
        db_comment="Data e hora de quando foi realizada a coleta",
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
    )

    amostragem = models.PositiveIntegerField(
        verbose_name="amostragem",
        default=0,

    )

    def __str__(self):
        return f'{self.id}{self.ordem} - {self.date}'