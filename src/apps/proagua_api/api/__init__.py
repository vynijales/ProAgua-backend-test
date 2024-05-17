from ninja import NinjaAPI
from ninja.security import django_auth
import requests

from . import (
    csrf,
    edificacoes,
    pontos,
    coletas,
    sequencia_coletas,
    usuarios,
    fluxos,
    parametros_referencia
)

# api = NinjaAPI(auth=django_auth, csrf=True)
api = NinjaAPI(auth=None, csrf=False)
api.add_router("/csrf", csrf.router)
api.add_router("/edificacoes", edificacoes.router)
api.add_router("/pontos", pontos.router)
api.add_router("/sequencias", sequencia_coletas.router)
api.add_router("/coletas", coletas.router)
api.add_router("/parametros_referencia", parametros_referencia.router)
api.add_router("/usuarios", usuarios.router)
api.add_router("/fluxos", fluxos.router)