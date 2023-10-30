from django.contrib.auth.models import User
from ninja import ModelSchema


class UsuarioIn(ModelSchema):
    class Config:
        model = User
        model_fields = ["username", "first_name", "last_name", "password", "is_staff", "email"]


class UsuarioOut(ModelSchema):
    class Config:
        model = User
        model_exclude = ["password", "user_permissions", "last_login"]
