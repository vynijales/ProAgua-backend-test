from ninja import NinjaAPI

from . import (
    auth,
    csrf,
    edificacoes,
    pontos,
    coletas,
    sequencia_coletas,
    usuarios,
    fluxos,
    parametros_referencia,
    solicitacoes
)

# api = NinjaAPI(auth=auth.JWTBearer(), csrf=False)
api = NinjaAPI(auth=None, csrf=False)

# Public routes
api.add_router("/auth", auth.router)
api.add_router("/csrf", csrf.router)

# Private routes
api.add_router("/edificacoes", edificacoes.router)
api.add_router("/pontos", pontos.router)
api.add_router("/sequencias", sequencia_coletas.router)
api.add_router("/coletas", coletas.router)
api.add_router("/parametros_referencia", parametros_referencia.router)
api.add_router("/usuarios", usuarios.router)
api.add_router("/fluxos", fluxos.router)
api.add_router("/solicitacoes", solicitacoes.router)