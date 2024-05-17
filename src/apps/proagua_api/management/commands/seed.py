import os
import django
import re
import pandas as pd

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from datasync.excel_utils import obter_dados_excel

from apps.proagua_api import models

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

class Command(BaseCommand):
    help = 'Seed data for the application'

    def create_edificacao(self, cronograma, codigo, nome, campus):
        codigos_existentes = set(models.Edificacao.objects.values_list('codigo', flat=True))

        if codigo in codigos_existentes:
            self.stdout.write(f"Dados já existentes para código {codigo}")
        else:
            edificacao = models.Edificacao.objects.create(
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

    def create_ponto(self, edificacao, ambiente, tipo, tombo, amontante = None):
        # Checa se o ponto existe, tendo como parâmetros edificacao, ambiente, tipo e amontante como chaves compostas
        ponto_exists = models.PontoColeta.objects.filter(
            edificacao=edificacao,
            ambiente=ambiente,
            tipo=tipo,
            amontante=amontante
        ).exists()

        if ponto_exists:
            self.stdout.write(f"Já existe um ponto com esses atributos: "
                                                 f"Edificacao: {edificacao}, "
                                                 f"Ambiente: {ambiente}, "
                                                 f"Tipo: {tipo}, "
                                                 "Tombo: {tombo}"
                                                 f"Amontante: {amontante}")
        else:
            # Cria um novo objeto PontoColeta
            ponto = models.PontoColeta.objects.create(
                edificacao=edificacao,
                ambiente=ambiente,
                tipo=tipo,
                tombo = tombo,
                amontante=amontante
            )

            if ponto:
                self.stdout.write(self.style.SUCCESS(f"{ponto} criado com sucesso."))
            else:
                self.stdout.write(self.style.ERROR("Erro ao criar o {ponto}."))  
    
    def create_pontos(self):
        # Criação de pontos de coleta

        df = obter_dados_excel(sheet_name="Lista de pontos")

        for indice, linha in df.iterrows():
            if indice <= 5:
                continue

            edificacao = models.Edificacao.objects.get(codigo=linha.iloc[0])

            if 'bebedouro' in str(linha.iloc[3]):
                tipo = 1
            elif 'torneira' in str(linha.iloc[3]):
                tipo = 2
            else:
                continue

            ambiente = linha.iloc[4]
            tombo = linha.iloc[5]

            self.create_ponto(edificacao, ambiente, tipo, tombo)

    DEFAULT_PASSWORD = '12345678'

    def create_user(self, username):
        try:
            if not User.objects.filter(username=username).exists():
                novo_usuario = User(username=username, password=self.DEFAULT_PASSWORD)
                novo_usuario.save()  # Salvar o usuário no banco de dados
                self.stdout.write(self.style.SUCCESS(f"Novo usuário criado: {username}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao criar usuário {username}: {e}"))

    def create_responsaveis(self):
        df = obter_dados_excel()

        for indice, linha in df.iterrows():
            if indice <= 5:
                continue

            if pd.notna(linha.iloc[12]):  # Verifica se a coluna na posição 12 não é NaN
                responsaveis = str(linha.iloc[11])  # Evita erros se a coluna não existir

                if responsaveis and responsaveis.lower() != 'nan':
                    # Substitui vírgulas, "e" e pontos por espaços
                    responsaveis = responsaveis.replace(',', ' ').replace(' e ', ' ').replace('.', '')

                    # Divide a string em uma lista de nomes não vazios
                    nomes = [nome for nome in responsaveis.split() if nome.strip()]
                    for nome in nomes:
                        self.create_user(nome)

    def create_parametros_referencia(self):
        referencia = models.ParametrosReferencia.objects.create(
            min_temperatura=9.5,
            max_temperatura=10.5,
            min_cloro_residual_livre=0.2,
            max_cloro_residual_livre=5.0,
            min_turbidez=None,
            max_turbidez=5.0,
            coliformes_totais=False,
            escherichia=False
        )

        if referencia:
            self.stdout.write(self.style.SUCCESS(f"Parâmetros de referência criados com sucesso."))
        else:
            self.stdout.write(self.style.ERROR("Erro ao criar os parâmetros de referência."))


    def create_sequencia(self, amostragem, ponto=None):
        object = models.SequenciaColetas.objects.create(amostragem=amostragem, ponto=ponto)

        if object:
            self.stdout.write(self.style.SUCCESS(f"{object} criado com sucesso."))
        else:
            self.stdout.write(self.style.ERROR("Erro ao criar o {ponto}.")) 

    def create_sequencias(self):
        df = obter_dados_excel()

        for indice, linha in df.iterrows():
            if indice <= 5:
                continue  # Pula as primeiras 6 linhas (índices 0 a 5)

            amostragem_ordinal = linha.iloc[0]

            if amostragem_ordinal.lower() in "primeira":
                amostragem = 1
            elif amostragem_ordinal.lower() in "segunda":
                amostragem = 2

            self.create_sequencia(amostragem=amostragem)

    def create_coleta(self, sequencia, ponto, responsaveis,
                       temperatura, coliformes_totais, escherichia, cor, data, ordem = "Coleta",
                        cloro_residual_livre = False, turbidez = False):
        try:
            coleta = models.Coleta.objects.create(
                sequencia=sequencia,
                ponto=ponto,
                temperatura=temperatura,
                cloro_residual_livre=cloro_residual_livre,
                turbidez=turbidez,
                coliformes_totais=coliformes_totais,
                escherichia=escherichia,
                cor=cor,
                data=data,
                ordem=ordem
            )
            coleta.responsavel.set(responsaveis)
            coleta.save()
            self.stdout.write(self.style.SUCCESS(f"Coleta criada com sucesso: {coleta}"))
    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao criar coleta: {e}"))

    def create_coletas(self):
        df = obter_dados_excel()

        for indice, linha in df.iterrows():
            if indice <= 5:
                continue

            id = indice - 5

            sequencia = models.SequenciaColetas.objects.get(id=id)
            try:
                ponto = models.PontoColeta.objects.get(id=1)
            except models.PontoColeta.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"PontoColeta with ID {id} does not exist."))

            lista_responsaveis = []
            temperatura = linha.iloc[12]
            cloro_residual_livre = linha.iloc[13]
            turbidez = linha.iloc[14]
            
            if linha.iloc[15] == "Presença":
                coliformes_totais = True
            else:
                coliformes_totais = False
            
            if linha.iloc[16] == "Presença":
                escherichia = True
            else:
                escherichia = False
            cor= linha.iloc[17]
            data= linha.iloc[9]
            hora= linha.iloc[10]

            ordem= "Coleta"

            if pd.notna(linha.iloc[12]) and pd.notna(linha.iloc[13]) and pd.notna(linha.iloc[14]) and pd.notna(linha.iloc[15]) and pd.notna(linha.iloc[16]) and pd.notna(linha.iloc[17]):
                self.create_coleta(sequencia, ponto, lista_responsaveis, temperatura, coliformes_totais, escherichia, cor, data, ordem, cloro_residual_livre, turbidez)
                coleta = models.Coleta.objects.create(
                sequencia=sequencia,
                ponto=ponto,
                temperatura=temperatura,
                cloro_residual_livre=cloro_residual_livre,
                turbidez=turbidez,
                coliformes_totais=coliformes_totais,
                escherichia=escherichia,
                cor=cor,
                data=data,
                ordem=ordem
            )

                coleta.responsavel.set(lista_responsaveis)



    def handle(self, *args, **options):
        self.create_edificacoes()
        self.create_pontos()
        self.create_responsaveis()
        self.create_parametros_referencia()
        self.create_sequencias()
        self.create_coletas()
        self.stdout.write(self.style.SUCCESS('Seed data created successfully.'))

if __name__ == '__main__':
    command = Command()
    command.handle()
