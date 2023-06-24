import os
import django
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.management.base import BaseCommand
from proagua.models import Edificacao, PontoColeta, Coleta


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

class Command(BaseCommand):
    help = 'Seed data for the application'

    def handle(self, *args, **options):

        # Criação de usuários
        admin = User.objects.create_superuser("admin", password="admin")
        user1 = User.objects.create_user('user1', password='password1')
        user2 = User.objects.create_user('user2', password='password2')

        # Criação de objetos Edificacao
        edificacao1 = Edificacao.objects.create(
            codigo='EDIF1',
            nome='Lab. Computação (LCC)',
            bloco='L'
        )
        edificacao2 = Edificacao.objects.create(
            codigo='EDIF2',
            nome='Centro de Engenharias (CE)',
            bloco='L'
        )

        # Criação de objetos PontoColeta
        
        ponto1 = PontoColeta.objects.create(
            edificacao=edificacao1,
            ambiente='Reservatório Inferior',
            tipo='RI',
            mes=1,
            pai=None
        )
        
        ponto2 = PontoColeta.objects.create(
            edificacao=edificacao1,
            ambiente='Reservatório Superior',
            tipo='RS',
            mes=1,
            pai=ponto1
        )
        
        ponto3 = PontoColeta.objects.create(
            edificacao=edificacao1,
            ambiente='Primeiro andar do prédio',
            tipo='BE',
            mes=1,
            pai=ponto2
        )

        ponto4 = PontoColeta.objects.create(
            edificacao=edificacao2,
            ambiente='Reservatório Inferior',
            tipo='RI',
            mes=2,
            pai=None
        )

        ponto5 = PontoColeta.objects.create(
            edificacao=edificacao2,
            ambiente='Reservatório Superior',
            tipo='RS',
            mes=2,
            pai=ponto4
        )

        ponto6 = PontoColeta.objects.create(
            edificacao=edificacao2,
            ambiente='Banheiro Feminino, térreo',
            tipo='TO',
            mes=2,
            pai=ponto5
        )

        ponto7 = PontoColeta.objects.create(
            edificacao=edificacao2,
            ambiente='Banheiro masculino, primeiro andar',
            tipo='TO',
            mes=2,
            pai=ponto5
        )

        # Criação de objetos Coleta
    
        now = timezone.now()

        coleta1 = Coleta.objects.create(
        ponto_coleta=ponto1,
        temperatura=25.3,
        cloro_residual_livre=1.6,
        cloro_total=2.2,
        turbidez=5.1,
        coliformes_totais=True,
        escherichia=False,
        cor='Azul',
        date=now,
        ordem='C',
        amostragem=1
    )
        coleta1.responsavel.add(user1, user2)

        coleta2 = Coleta.objects.create(
            ponto_coleta=ponto2,
            temperatura=36.2,
            cloro_residual_livre=1.1,
            cloro_total=1.9,
            turbidez=4.7,
            coliformes_totais=False,
            escherichia=False,
            cor='Vermelho',
            date=now,
            ordem='C',
            amostragem=1
        )
        coleta2.responsavel.add(user2)

        coleta3 = Coleta.objects.create(
            ponto_coleta=ponto3,
            temperatura=26.4,
            cloro_residual_livre=1.2,
            cloro_total=1.7,
            turbidez=4.8,
            coliformes_totais=False,
            escherichia=False,
            cor='Vermelho',
            date=now,
            ordem='C',
            amostragem=1
        )
        coleta3.responsavel.add(user2)


        coleta4 = Coleta.objects.create(
            ponto_coleta=ponto4,
            temperatura=26.6,
            cloro_residual_livre=1.3,
            cloro_total=1.6,
            turbidez=4.6,
            coliformes_totais=False,
            escherichia=False,
            cor='Vermelho',
            date=now,
            ordem='C',
            amostragem=1
        )
        coleta4.responsavel.add(user1, user2)

        coleta5 = Coleta.objects.create(
            ponto_coleta=ponto5,
            temperatura=26.8,
            cloro_residual_livre=1.4,
            cloro_total=1.5,
            turbidez=4.4,
            coliformes_totais=False,
            escherichia=False,
            cor='Vermelho',
            date=now,
            ordem='C',
            amostragem=1
        )

        coleta5.responsavel.add(user1, user2)

        coleta6 = Coleta.objects.create(
            ponto_coleta=ponto6,
            temperatura=27.0,
            cloro_residual_livre=1.5,
            cloro_total=1.4,
            turbidez=4.2,
            coliformes_totais=False,
            escherichia=False,
            cor='Vermelho',
            date=now,
            ordem='R',
            amostragem=1
        )

        coleta6.responsavel.add(user1, user2)

        coleta7 = Coleta.objects.create(
            ponto_coleta=ponto7,
            temperatura=26.0,
            cloro_residual_livre=1.0,
            cloro_total=1.8,
            turbidez=4.5,
            coliformes_totais=False,
            escherichia=False,
            cor='Vermelho',
            date=now,
            ordem='R',
            amostragem=1
        )

        coleta7.responsavel.add(user1, user2)

        self.stdout.write(self.style.SUCCESS('Seed data created successfully.'))

if __name__ == '__main__':
    command = Command()
    command.handle()