import os
import django
import re
import pandas as pd

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from datasync.excel_utils import obter_dados_excel

from apps.proagua_api.models.edificacao import Edificacao

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

class Command(BaseCommand):
    help = 'Seed data for the application'

    def create_edificacao(self, cronograma, codigo, nome, campus):
        codigos_existentes = set(Edificacao.objects.values_list('codigo', flat=True))

        if codigo in codigos_existentes:
            self.stdout.write(f"Dados já existentes para código {codigo}")
        else:
            edificacao = Edificacao.objects.create(
                cronograma=cronograma,
                codigo=codigo,
                nome=nome,
                campus=campus
            )
            if edificacao:
                self.stdout.write(self.style.SUCCESS(f"Edificação de código {codigo} criada com sucesso."))
                codigos_existentes.add(codigo)
            else:
                self.stdout.write(self.style.ERROR(f"Erro ao criar Edificacao para código {codigo}"))

    def create_edificacoes(self):
        # Criação de edificações

        df = obter_dados_excel()

        for indice, linha in df.iterrows():
            if indice <= 5:
                continue  # Pula as primeiras 6 linhas (índices 0 a 5)

            campus = linha.iloc[5]
            if campus == 'Leste':
                campus = 'LE'
            elif campus == 'Oeste':
                campus = 'OE'

            cronograma = int(re.search(r'\d+', linha.iloc[2]).group())
            codigo = linha.iloc[3]
            nome = linha.iloc[4]

            self.create_edificacao(cronograma, codigo, nome, campus)

    def handle(self, *args, **options):
        
        self.create_edificacoes()
        self.stdout.write(self.style.SUCCESS('Seed data created successfully.'))

if __name__ == '__main__':
    command = Command()
    command.handle()
