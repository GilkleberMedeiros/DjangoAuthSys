from home import settings

class SendValidateEmailMixin:
    email_template = "emails/email_validate.html"
    from_email = settings.DEFAULT_FROM_EMAIL
    email_subject = "Validate your email"
    __email_context = {}
    email_extra_context = {}
    _token_bytes_lenght = 32

    def generate_token(self):
        import secrets

        token = secrets.token_hex(self._token_bytes_lenght)

        return token
    
    def set_context(self):
        from datetime import datetime

        self.__email_context["username"] = self.user.username
        self.__email_context["time"] = datetime.now()
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
