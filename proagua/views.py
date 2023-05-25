from django.shortcuts import render

# Create your views here.

def home(request):
    return render(
        request=request,
        template_name="landing_page.html"
    )


def login(request):
    return render(
        request=request,
        template_name="login.html"
    )

def privado(request):
    return render(
        request=request,
        template_name="privado/coletas.html"
    )
