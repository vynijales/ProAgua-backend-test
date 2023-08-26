from django.db import models
from django.contrib.auth.models import User

class Edificacao(models.Model):
    codigo = models.CharField(
        verbose_name="código",
        max_length=8,
        primary_key=True)
    nome = models.CharField(
        verbose_name="nome",
        max_length=30)
    campus = models.CharField(
        verbose_name="campus",
        max_length=2,
        choices=(("LE", "Leste"), ("OE", "Oeste")),
        default=(("LE", "Leste")))
    cronograma = models.PositiveIntegerField(
        verbose_name="cronograma",
    )

    def __str__(self) -> str:
        return f"Edificacao {self.codigo}"

class Ponto(models.Model):
    id = models.AutoField(primary_key=True)
    edificacao = models.ForeignKey(
        to=Edificacao,
        related_name="Ponto",
        verbose_name="código da edificação", 
        on_delete=models.PROTECT,
        blank=False)
    ambiente = models.CharField(
        verbose_name="ambiente",
        max_length=20)
    tipo = models.IntegerField(
        verbose_name="tipo",
        choices=(
            (1, "Bebedouro"),
            (2, "Reservatório predial superior"),
            (3, "Reservatório predial inferior"),
            (4, "Reservatório de distribuição superior"),
            (5, "Reservatório de distribuição inferior"),
            (6, "CAERN")
        ),
        default=(1, "Bebedouro")
    )
    amontante = models.ForeignKey(
        to="Ponto",
        verbose_name="ponto amontante",
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return f"Ponto {self.id}"

class SequenciaColetas(models.Model): 
    id = models.AutoField(primary_key=True)
    amostragem = models.PositiveIntegerField(
        verbose_name="amostragem"
    )

    def __str__(self) -> str:
        return f"Sequencia Coletas {self.id}"

class Coleta(models.Model):
    id = models.AutoField(primary_key=True)
    sequencia = models.ForeignKey(
        to=SequenciaColetas,
        verbose_name="sequência de Coletas",
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    ponto = models.ForeignKey(
        to=Ponto,
        verbose_name="Ponto de Coleta",
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    temperatura = models.FloatField(
        verbose_name="temperatura",
    )
    cloro_residual_livre = models.FloatField(
        verbose_name="cloro residual livre",
    )
    turbidez = models.FloatField(
        verbose_name="turbidez",
    )
    coliformes_totais = models.BooleanField(
        verbose_name="coliformes totais",
    )
    escherichia = models.BooleanField(
        verbose_name="escherichia coli",
    )
    date = models.DateTimeField(
        verbose_name="data da coleta",
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

    def __str__(self) -> str:
        return f"Coleta {self.id}"
  