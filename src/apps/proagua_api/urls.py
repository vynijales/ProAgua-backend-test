from django.urls import path
from . import api

urlpatterns = [
    path('api/v1/', api.api.urls)
]
