from django.db import models

class PontoColeta(models.Model):
    id = models.AutoField(primary_key=True)
    edificacao = models.ForeignKey(
        to="Edificacao",
        related_name="PontoColeta",
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
        to="PontoColeta",
        verbose_name="ponto amontante",
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return f"Ponto {self.id}"
