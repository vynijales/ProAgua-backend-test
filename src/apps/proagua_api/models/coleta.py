from django.db import models
from django.contrib.auth.models import User


class Coleta(models.Model):
    id = models.AutoField(primary_key=True)
    sequencia = models.ForeignKey(
        to="SequenciaColetas",
        verbose_name="sequência de Coletas",
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    ponto = models.ForeignKey(
        to="PontoColeta",
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
    cor = models.FloatField(
        verbose_name="cor"
    )
    data = models.DateTimeField(
        verbose_name="data da coleta",
    )
    responsavel = models.ManyToManyField(
        to=User,
        verbose_name="responsaveis",
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
  