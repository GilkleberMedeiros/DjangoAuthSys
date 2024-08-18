from home import settings

class SendValidationEmailMixin:
    email_template = "emails/email_validate.html"
    from_email = settings.DEFAULT_FROM_EMAIL
    email_subject = "Validate your email"
    __email_context = {}
    email_extra_context = {}
    _token_bytes_lenght = 32

    def generate_token(self):
        import secrets

        token = secrets.token_hex(self._token_bytes_lenght)
        self.store_token(token)

        return token
    
    def store_token(self, token: str):
        settings.VALIDATION_EMAILS_SENT[self.user.username] = token
    
    def set_context(self):
        from datetime import datetime

        self.__email_context["username"] = self.user.username
        self.__email_context["datetime"] = datetime.now()
        self.__email_context["token"] = self.generate_token()
        self.__email_context.update(self.email_extra_context)

    def render_email(self):
        from django.template.loader import render_to_string

        return render_to_string(self.email_template, self.__email_context)
    
    def send_email(self, user=None):
        if user is None:
            try: user = self.object
            except: raise AttributeError("User object doesn't exists and was not passed!")
        
        self.user = user

        self.set_context()
        email_str = self.render_email()

        user.email_user(self.email_subject, email_str, self.from_email)


class ConfirmValidationEmailMixin:
    confirm_failed_template = "emails/failed_confirm.html"
    confirm_success_template = "emails/success_confirm.html"
    __context = {}
    extra_context = {}

    def valid_email(self, request, user, token: str, datetime):
        from datetime import datetime as dt
        from django.shortcuts import render
        from .utils import is_permission_created_create
        from .models import Dummy

        miliseconds_passed = ((dt.now() - datetime).total_seconds() * 1000)

        if miliseconds_passed > settings.EMAIL_VALIDATE_MESSAGE_AGE:
            self.__context["fail_message"] = "this link is expired"
            self.__context.update(self.extra_context)

            return render(request, self.confirm_failed_template, self.__context)
        elif not settings.VALIDATION_EMAILS_SENT.get(user.username, "") == token:
            self.__context["fail_message"] = "this link is not the same that was sent to you or is some old link"
            self.__context.update(self.extra_context)

            return render(request, self.confirm_failed_template, self.__context)
        elif user.email_validated:
            self.__context["fail_message"] = "your email is already validated"
            self.__context.update(self.extra_context)

            return render(request, self.confirm_failed_template, self.__context)
        else:
            self.__context["success_message"] = "your email is now validated"
            self.__context.update(self.extra_context)

            user.email_validated = True
            perm = is_permission_created_create(
                "valid_email", "O usuário tem um email validado", 
                Dummy
            )
            user.user_permissions.add(perm)

            return render(request, self.confirm_success_template, self.__context)

