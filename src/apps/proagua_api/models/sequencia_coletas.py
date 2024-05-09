from django.db import models

class SequenciaColetas(models.Model): 
    id = models.AutoField(primary_key=True)
    amostragem = models.PositiveIntegerField(
        verbose_name="amostragem"
    )
    ponto = models.ForeignKey(
        to="proagua_api.PontoColeta",
        verbose_name="ponto",
        on_delete=models.PROTECT,
    )
    
    class Meta:
        unique_together  = ("amostragem", "ponto")
    
    def __str__(self) -> str:
        return f"Sequencia Coletas {self.id}"
