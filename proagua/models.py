from django.db import models

# Create your models here.

class Edificacao(models.Model):
    codigo = models.CharField(
        verbose_name='código',
        max_length=20
    )
    nome = models.CharField(
        verbose_name='nome da edificação',
        max_length=80
    )


class PontoColeta(models.Model):
    edificacao = models.ForeignKey(
        to=Edificacao,
        verbose_name='edificação',
        on_delete=models.CASCADE
    )
    ambiente = models.CharField(
        verbose_name='ambiente',
        max_length=120
    )
    torneira = models.BooleanField(
        verbose_name='torneira'
    )

    def __str__(self):
        return f'Ponto de Coleta - {self.edificacao.nome} - {self.ambiente}'
