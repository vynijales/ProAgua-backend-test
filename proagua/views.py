from django.shortcuts import render
from .models import PontoColeta
# Create your views here.

def home(request):
    return render(
        request=request,
        template_name="landing_page.html"
    )

def coletas(request):
    context = {
        'pontos_coletas': PontoColeta.objects.all()
    }

    return render(
        request=request,
        template_name="privado/coletas.html",
        context=context
    )
