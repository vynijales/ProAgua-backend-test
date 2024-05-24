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

