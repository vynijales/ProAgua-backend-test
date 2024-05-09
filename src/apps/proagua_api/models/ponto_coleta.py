from django.db import models
from .coleta import Coleta

TIPOS_PONTOS = (
    (1, "Bebedouro"),
    (2, "Reservatório predial superior"),
    (3, "Reservatório predial inferior"),
    (4, "Reservatório de distribuição superior"),
    (5, "Reservatório de distribuição inferior"),
    (6, "CAERN")
)


class PontoColeta(models.Model):
    id = models.AutoField(primary_key=True)
    imagem = models.ImageField(
        upload_to="media/images/pontos",
        blank=True,
        null=True
    )
    
    edificacao = models.ForeignKey(
        to="Edificacao",
        related_name="PontoColeta",
        verbose_name="código da edificação",
        on_delete=models.PROTECT,
        blank=False
    )

    ambiente = models.CharField(
        verbose_name="ambiente",
        max_length=20
    )

    tipo = models.IntegerField(
        verbose_name="tipo",
        choices=TIPOS_PONTOS,
        default=(1, "Bebedouro")
    )

    tombo = models.CharField(
        max_length=20,
        verbose_name="tombo",
        blank=True,
        null=True
    )

    amontante = models.ForeignKey(
        to="PontoColeta",
        verbose_name="ponto amontante",
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    imagem = models.ImageField(
        upload_to="media/images/edificacoes",
        blank=False,
        null=False
    )

    def status(self) -> bool | None:
        coleta = Coleta.objects.filter(ponto=self).last()
        if coleta:
            return coleta.status

    def status_message(self) -> str | None:
        coleta = Coleta.objects.filter(ponto=self).last()
        if coleta:
            return coleta.status_message

    def __str__(self) -> str:
        return f"Ponto {self.id} - {self.get_tipo_display()}"
