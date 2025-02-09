from django.http import HttpRequest
from django.shortcuts import render

from django.contrib.auth.views import (
    LoginView, 
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import (
    login_required, 
    permission_required, 
)
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView, View

from .forms import UserSignUpModelForm
from .models import Dummy, CustomUser
from .utils import is_permission_created_create
from .mixins import (
    SendValidationEmailMixin, 
    ConfirmValidationEmailMixin, 
)
from .decorators import email_required

from django.http.response import (
    HttpResponse, 
    HttpResponseRedirect,
    HttpResponseNotFound,
)

# Create your views here.
def home(request):
    return render(request, "home.html")

@login_required
@email_required
def pag1(request):
    return render(request, "pag1.html")

@login_required
@email_required
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

        try: user = CustomUser.objects.get(pk=user_new_data["id"])
        except: return HttpResponseNotFound("Usuário não existe!")

        for key, value in user_new_data.items():
            if key != "password":
                user.__setattr__(key, value)
                continue

            user.set_password(value)

        user.save()

        return HttpResponseRedirect(reverse_lazy('profile_changes_done'))
    

class ChangeDone(TemplateView):
    template_name = "user_data_altered_done.html"


class LogIn(LoginView):
    template_name = "login.html"


class LogOut(LogoutView):
    template_name = "logout.html"

    def get_redirect_url(self):
        return reverse_lazy("home")


class SignUp(SuccessMessageMixin, SendValidationEmailMixin, CreateView):
    template_name = "signup.html"
    model = CustomUser
    success_url = reverse_lazy("validation_email_sent")
    form_class = UserSignUpModelForm
    success_message = "Sua Conta foi registrada com sucesso!"

    email_subject = "Valide seu email no [SITE]"

    def form_valid(self, form):
        r = super().form_valid(form)

        if form.cleaned_data["prime_user_permission"]:
            perm = is_permission_created_create("view_pag2", "Ver a página 2", Dummy)
            self.object.user_permissions.add(perm)
            self.object.save()

        self.send_email(self.object)

        return r
    

class ValidationEmailSent(TemplateView):
    template_name = "emails/validation_email_sent.html"
    next_page = reverse_lazy("login")

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["next_page"] = self.next_page

        return context
    
class SendValidationEmail(SendValidationEmailMixin, ValidationEmailSent):
    next_page = reverse_lazy("profile")
    email_subject = "Valide seu email no [SITE]"

    def get(self, request: HttpRequest, *args: tuple[any], **kwargs: dict[any, any]) -> HttpResponse:
        self.send_email(user=request.user)

        return super().get(request, *args, **kwargs)

    
class ConfirmEmail(LoginRequiredMixin, ConfirmValidationEmailMixin, View):
    
    def get(self, request, *args, **kwargs) -> HttpResponse:
        user = request.user
        token = request.GET["token"]
        datetime = request.GET["datetime"]

        return self.valid_email(request, user, token, datetime)
    

class PasswordReset(PasswordResetView):
    template_name = "password_reset.html"
    email_template_name = "emails/password_reset_plain_text.html"
    html_email_template_name = "emails/password_reset.html"


class PasswordResetDone(PasswordResetDoneView):
    template_name = "password_reset_done.html"


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = "password_reset_confirm.html"


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = "password_reset_complete.html"
