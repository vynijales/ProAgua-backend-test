from django.db import models
from django.contrib.auth.models import User

import csv
from io import StringIO

BEBEDOURO = 1
RPS = 2
RPI = 3
RDS = 4
RDI = 5
CAERN = 6


class Coleta(models.Model):
    id = models.AutoField(primary_key=True)
    sequencia = models.ForeignKey(
        to="SequenciaColetas",
        verbose_name="sequência de Coletas",
        related_name="coletas",
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    ponto = models.ForeignKey(
        to="PontoColeta",
        verbose_name="Ponto de Coleta",
        on_delete=models.PROTECT,
        related_name="coletas",
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

    def status(self) -> str:
        status_temperatura = self.analise_temperatura()
        status_turbidez = self.analise_turbidez()
        status_coliformes = self.analise_coliformes()
        status_escherichia = self.analise_escherichia()

        if not status_temperatura.get("status"):
            return status_temperatura

        if not status_turbidez.get("status"):
            return status_turbidez

        if not status_coliformes.get("status"):
            return status_coliformes

        if not status_escherichia.get("status"):
            return status_escherichia

        return {
            "status": True,
            "message": "Qualidade adequada para uso"
        }

    def analise_temperatura(self):
        MARGEM_TEMPERATURA = 5

        if self.ponto.tipo == BEBEDOURO:
            if self.temperatura < 9.5:
                return {
                    "status": False,
                    "message": "Temperatura desconforme"
                }
            elif self.temperatura > 10.5:
                return {
                    "status": False,
                    "message": "Temperatura desconforme. Solicitar manutenção"
                }
            else:
                return {
                    "status": True,
                    "message": "Bebedouro funcionando"
                }
        else:
            if abs(self.temperatura - 37) > MARGEM_TEMPERATURA:
                return {
                    "status": False,
                    "message": "Temperatura desconforme"
                }
            else:
                return {
                    "status": True,
                    "message": "Água adequada para uso"
                }

    def analise_turbidez(self):
        if self.turbidez <= 5:
            return {
                "status": True,
                "message": "Turbidez adequada"
            }
        else:
            return {
                "status": False,
                "message": "Turbidez inadequada"
            }

    def analise_coliformes(self):
        if self.coliformes_totais:
            return {
                "status": False,
                "message": "Presença de coliformes"
            }
        else:
            return {
                "status": True,
                "message": "Ausencia de coliformes"
            }

    def analise_escherichia(self):
        if self.escherichia:
            return {
                "status": False,
                "message": "Presença de escherichia coli."
            }
        else:
            return {
                "status": True,
                "message": "Ausência de escherichia coli."
            }

    def get_csv(self):
        field_names = [field.name for field in self._meta.fields]

        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=field_names)

        writer.writeheader()
        writer.writerow({field: getattr(self, field) for field in field_names})

        return output.getvalue()

    def __str__(self) -> str:
        return f"Coleta {self.id}"
