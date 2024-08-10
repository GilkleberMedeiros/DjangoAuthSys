from django.shortcuts import render

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Model
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import UserSignUpModelForm
from .models import Dummy

from django.http.response import HttpResponse

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

@login_required
def profile(request):
    return HttpResponse("Nothing here!")


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


def is_permission_created(permission_codename: str, permission_name: str = None, model_or_contentType: Model = None):
    if model_or_contentType is not None:
        model_or_contentType = get_content_type_from_model(model_or_contentType)
    
    try: 
        perm = Permission.objects.get(
        codename=permission_codename, 
        name=permission_name,
        content_type=model_or_contentType
        )
    except: return False

    return perm

def get_content_type_from_model(model: Model):
    from django.contrib.contenttypes.models import ContentType

    content_type = model
    if not issubclass(model.__class__, ContentType):
        content_type = ContentType.objects.get_for_model(model)
    
    return content_type

def create_permission(codename: str, name: str, model_or_contentType: Model):
    content_type = get_content_type_from_model(model_or_contentType)

    permission = Permission.objects.create(
        codename=codename,
        name=name,
        content_type=content_type,
    )

    return permission

def is_permission_created_create(codename: str, name: str, model_or_contentType: Model):
    if not (perm_or_false := is_permission_created(codename, 
        permission_name=name, 
        model_or_contentType=model_or_contentType)):
        perm = create_permission(codename, name, model_or_contentType)

        return perm
    
    return perm_or_false