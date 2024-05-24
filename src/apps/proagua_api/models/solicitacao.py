from django.db import models

from enum import Enum

class Status(Enum):
    PENDENTE = "Pendente"
    ENVIADO = "Enviado"

class TipoSolicitacao(Enum):
    LIMPEZA_RESERVATORIO = "Limpeza de reservatório"
    INSTALACAO_PONTO = "Instalação de ponto de coleta"
    CONSERTO_RESERVATORIO = "Conserto de reservatório"

class Solicitacao(models.Model):
    ponto = models.ForeignKey(
        to="PontoColeta",
        related_name="Solicitacao",
        verbose_name="ponto de coleta",
        on_delete=models.PROTECT,
        blank=False
    )
    data = models.DateTimeField(
        verbose_name="data da solicitação",
        auto_now_add=True
    )
    status = models.CharField(
        verbose_name="status",
        max_length=50,
        choices=[(tag, tag.value) for tag in Status],
        default=Status.PENDENTE
    )
    observacao = models.TextField(
        verbose_name="observação",
        max_length=1250,
        blank=True,
        null=True
    )
    justificativa = models.TextField(
        verbose_name="justificativa",
        max_length=1250,
        blank=True,
        null=True
    )
