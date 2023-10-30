from typing import List

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from .schemas.usuario import UsuarioOut, UsuarioIn

router = Router()


@router.get("/", response=List[UsuarioOut])
@paginate
def list_usuario(request):
    qs = User.objects.all()
    return qs


@router.get("/{username}", response=UsuarioOut)
def get_usuario(request, username: str):
    usuario = get_object_or_404(User, username=username)
    return usuario

@router.post("/")
def create_usuario(request, payload: UsuarioIn):
    # TODO: criar usuario
    pass

@router.put("/{username}")
def update_usuario(request):
    # TODO: atualizar usuario
    pass

@router.delete("/{username}")
def delete_usuario(request):
    # TODO: deletar usuario
    pass
