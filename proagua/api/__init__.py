from ninja import NinjaAPI
from ninja.security import django_auth

from .schema import *

from . import edificacoes, pontos

api = NinjaAPI(auth=django_auth, csrf=True)

api.add_router("/edificacoes/", edificacoes.router)
api.add_router("/pontos/", pontos.router)
