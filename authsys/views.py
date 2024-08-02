from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import UserSignUpModelForm

from django.http.response import HttpResponse

# Create your views here.
def home(request):
    return render(request, "home.html")

def pag1(request):
    return render(request, "pag1.html")

def pag2(request):
    return render(request, "pag2.html")

def profile(request):
    return HttpResponse("Nothing here!")


class LogIn(LoginView):
    template_name = "login.html"

class SignUp(SuccessMessageMixin, CreateView):
    template_name = "signup.html"
    model = User
    success_url = reverse_lazy("login")
    form_class = UserSignUpModelForm
    success_message = "Sua Conta foi registrada com sucesso!"