from ninja import Router
from django.middleware.csrf import get_token

router = Router()


@router.get("/")
def get_csrf_token(request):
    csrf_token = get_token(request)
    return {"csrf_token": csrf_token}
