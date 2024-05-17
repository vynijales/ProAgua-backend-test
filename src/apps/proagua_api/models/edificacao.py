from django.db import models
from .image import Image

class Edificacao(models.Model):
    imagens = models.ManyToManyField(to=Image)
    codigo = models.CharField(
        verbose_name="código",
        max_length=8,
        unique=True,
        null=False,
        blank=False
    )
    nome = models.CharField(
        verbose_name="nome",
        max_length=80)
    campus = models.CharField(
        verbose_name="campus",
        max_length=2,
        choices=(("LE", "Leste"), ("OE", "Oeste")),
        default=(("LE", "Leste"))
    )
    cronograma = models.PositiveIntegerField(
        verbose_name="cronograma",
    )

    def __str__(self) -> str:
        return f"Edificacao {self.codigo}"
