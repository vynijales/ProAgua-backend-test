import datetime

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings

from ninja.security import HttpBearer
from ninja import Router
from ninja import Schema

import jwt
from jwt import DecodeError, ExpiredSignatureError

class JWTBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            # Try to decode the token
            payload = jwt.decode(
                jwt=token,
                key=settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
        except DecodeError as e:
            # Do not authorize if there is a decode error
            print("Ops! There is a DecodeError:", str(e))
            return False
    
        except ExpiredSignatureError as e:
            # Do not authorize if the token is expired
            print("Ops! The token is expired")
            return False
        
        return payload


router = Router(tags=["Authentication"])

class LoginCredentialsSchema(Schema):
    username: str
    password: str


def generate_auth_token(user: User) -> str | None:
    if user is None:
        return None
    
    issued_at = datetime.datetime.now()
    expiration_time = issued_at + datetime.timedelta(days=1)

    token = jwt.encode(
        payload={
            "id": user.id,
            "username": user.username,
            "iat": int(issued_at.timestamp()),
            "exp": int(expiration_time.timestamp())
        },
        key=settings.JWT_SECRET_KEY,
        headers={
            "alg": settings.JWT_ALGORITHM,
            "typ": "JWT"
        }
    )

    return token


@router.post("/login", auth=None)
def login(request, credentials: LoginCredentialsSchema):
    user = authenticate(request, **credentials.dict())
    if user is not None:
        token = generate_auth_token(user)
        return {"access_token": token}
