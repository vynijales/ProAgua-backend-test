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


@router.post("/", response=UsuarioOut)
def create_usuario(request, payload: UsuarioIn):
    user = User.objects.create(**payload.dict())
    user.save()
    return user


@router.put("/{username}")
def update_usuario(request, username: str, payload: UsuarioIn):
    user = get_object_or_404(User, username=username)
    for attr, value in payload.dict().items():
        setattr(user, attr, value)
    user.save()
    return {"status": "success"}


@router.delete("/{username}")
def delete_usuario(request, username: str):
    user = get_object_or_404(User, username=username)
    user.delete()
    return {"status": "success"}
