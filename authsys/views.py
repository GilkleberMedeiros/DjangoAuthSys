from django.shortcuts import render

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import (
    login_required, 
    permission_required, 
)
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

from .forms import UserSignUpModelForm
from .models import Dummy
from .utils import is_permission_created_create

from django.http.response import (
    HttpResponse, 
    HttpResponseRedirect,
    HttpResponseNotFound,
)

# Create your views here.
def home(request):
    return render(request, "home.html")

@login_required
def pag1(request):
    return render(request, "pag1.html")

@login_required
@permission_required("dummy.view_pag2")
def pag2(request):
    return render(request, "pag2.html")

class Profile(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

    def post(self, request, *args, **kwargs):
        fields = ["id", "username", "first_name", "last_name", "email", "password"]
        user_new_data = {}

        for key in fields:
            try: user_new_data[key] = request.POST[key]
            except: pass

        try: user = User.objects.get(pk=user_new_data["id"])
        except: return HttpResponseNotFound("Usuário não existe!")

        for key, value in user_new_data.items():
            if key != "password":
                user.__setattr__(key, value)
                continue

            user.set_password(value)

        user.save()

        return HttpResponseRedirect(reverse_lazy('profile'))
    

class ChangeDone(TemplateView):
    template_name = "user_data_altered_done.html"


class LogIn(LoginView):
    template_name = "login.html"


class LogOut(LogoutView):
    template_name = "logout.html"

    def get_redirect_url(self):
        return reverse_lazy("home")


class SignUp(SuccessMessageMixin, CreateView):
    template_name = "signup.html"
    model = User
    success_url = reverse_lazy("login")
    form_class = UserSignUpModelForm
    success_message = "Sua Conta foi registrada com sucesso!"

    def form_valid(self, form):
        r = super().form_valid(form)

        if form.cleaned_data["prime_user_permission"]:
            perm = is_permission_created_create("view_pag2", "Ver a página 2", Dummy)
            self.object.user_permissions.add(perm)
            self.object.save()

        return r
