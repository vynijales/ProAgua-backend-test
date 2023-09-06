from django.db import models

class SequenciaColetas(models.Model): 
    id = models.AutoField(primary_key=True)
    amostragem = models.PositiveIntegerField(
        verbose_name="amostragem"
    )

    def __str__(self) -> str:
        return f"Sequencia Coletas {self.id}"
