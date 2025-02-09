from home.settings import (
    DEFAULT_FROM_EMAIL,
    VALIDATION_EMAILS_SENT,
    EMAIL_VALIDATE_MESSAGE_AGE,
    NON_EMAIL_VALIDATED_USER_AGE,
    LOGIN_URL,
)
from datetime import datetime as dt
from django.template.loader import render_to_string
from django.shortcuts import render
from .utils import is_permission_created_create
from .models import Dummy
from django.utils import timezone
from django.http import HttpResponseRedirect

class SendValidationEmailMixin:
    email_template = "emails/email_validate.html"
    from_email = DEFAULT_FROM_EMAIL
    email_subject = "Validate your email"
    email_confirm_url = "http://localhost:8000/profile/confirm/email/"
    datetime_str_format = "%d/%m/%y %H:%M:%S.%f"
    __email_context = {}
    email_extra_context = {}
    _token_bytes_lenght = 32

    def generate_token(self):
        import secrets

        token = secrets.token_hex(self._token_bytes_lenght)
        self.store_token(token)

        return token
    
    def store_token(self, token: str):
        VALIDATION_EMAILS_SENT[self.user.username] = token
    
    def set_context(self):
        self.__email_context["confirm_url"] = self.email_confirm_url
        self.__email_context["username"] = self.user.username
        self.__email_context["datetime"] = \
            dt.now().strftime(self.datetime_str_format)
        self.__email_context["token"] = self.generate_token()
        self.__email_context.update(self.email_extra_context)

    def render_email(self):
        return render_to_string(self.email_template, self.__email_context)
    
    def send_email(self, user=None):
        if user is None:
            try: user = self.object
            except: raise AttributeError("User object doesn't exists and was not passed!")
        
        self.user = user

        self.set_context()
        email_str = self.render_email()

        user.email_user(self.email_subject, self.from_email, html_message=email_str)


class ConfirmValidationEmailMixin:
    confirm_failed_template = "emails/failed_confirm.html"
    confirm_success_template = "emails/success_confirm.html"
    __context = {}
    extra_context = {}
    datetime_str_format = "%d/%m/%y %H:%M:%S.%f"

    def valid_email(self, request, user, token: str, datetime_str):
        datetime = dt.strptime(datetime_str, self.datetime_str_format)

        miliseconds_passed = ((dt.now() - datetime).total_seconds() * 1000)

        if miliseconds_passed > EMAIL_VALIDATE_MESSAGE_AGE:
            self.__context["fail_message"] = "Este link expirou"
            self.__context.update(self.extra_context)

            return render(request, self.confirm_failed_template, self.__context)
        elif not VALIDATION_EMAILS_SENT.get(user.username, "") == token:
            self.__context["fail_message"] = \
                "O nome de usuário de \
                quem está acessando este link não é o memso para o \
                qual este link foi mandado ou é algum link \
                antigo, tenha certeza de estar logado com \
                a conta correta ou não estar logado"
            self.__context.update(self.extra_context)

            return render(request, self.confirm_failed_template, self.__context)
        elif user.email_validated:
            self.__context["fail_message"] = "Seu email já está validado"
            self.__context.update(self.extra_context)

            return render(request, self.confirm_failed_template, self.__context)
        else:
            self.__context["success_message"] = "Seu email agora está validado"
            self.__context.update(self.extra_context)

            user.email_validated = True
            perm = is_permission_created_create(
                "valid_email", "O usuário tem um email validado", 
                Dummy
            )
            user.user_permissions.add(perm)
            user.save()

            VALIDATION_EMAILS_SENT.pop(user.username)

            return render(request, self.confirm_success_template, self.__context)


class EmailRequiredMixin:
    redirect_url = "/"

    def is_anonymoususer(self):
        return self.user.id is None
    
    def is_admin(self):
        return self.user.is_superuser or self.user.is_staff
    
    def get_email_valid(self):
        return self.user.email_validated
        
    def get_expired(self):
        td = timezone.now() - self.user.date_joined

        return td.total_seconds * 1000 > NON_EMAIL_VALIDATED_USER_AGE

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user

        if self.is_anonymoususer():
            return HttpResponseRedirect(LOGIN_URL)
        
        if self.is_admin():
            return super().dispatch(request, *args, **kwargs)
        
        if not self.get_email_valid() and self.get_expired():
            return HttpResponseRedirect(self.redirect_url)
        
        return super().dispatch(request, *args, **kwargs)