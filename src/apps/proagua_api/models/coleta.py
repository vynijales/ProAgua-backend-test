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
    status = models.BooleanField(
        verbose_name="status",
        default=None,
        null=True,
    )

    status_message = models.CharField(
        verbose_name="status message",
        max_length=200,
        default=None,
        null=True
    )

    def analise(self):
        status_temperatura = self.analise_temperatura()
        status_turbidez = self.analise_turbidez()
        status_coliformes = self.analise_coliformes()
        status_escherichia = self.analise_escherichia()
        
        status = {
            "status": True,
            "messages": []
        }

        if not status_coliformes["status"]:
            status["status"] = False
            status["messages"].append(status_coliformes["message"])

        if not status_escherichia["status"]:
            status["status"] = False
            status["messages"].append(status_escherichia["message"])

        if not status_turbidez["status"]:
            status["status"] = False
            status["messages"].append(status_turbidez["message"])

        if not status_temperatura["status"]:
            status["status"] = False
            status["messages"].append(status_temperatura["message"])

        if not status["status"]:
            return status

        return {
            "status": True,
            "messages": ["Qualidade adequada para uso"]
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
   
    @classmethod
    def get_csv(cls, coletas):
        field_names = [field.name for field in cls._meta.fields]
        csv_data = ""
        for coleta in coletas:
            csv_data += ",".join([str(getattr(coleta, field)) for field in field_names]) + "\n"
        return csv_data

    def save(self, *args, **kwargs):
        analise = self.analise()
        
        self.status = analise.get("status")
        self.status_message = ', '.join(analise.get("messages"))

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Coleta {self.id}"
