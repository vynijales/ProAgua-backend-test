from django.urls import path
from . import api_v1

urlpatterns = [
    path('api/v1/', api_v1.api.urls)
]
