from django.forms import Form, ModelForm, BooleanField

from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UsernameField


class UserSignUpModelForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True


    prime_user_permission = BooleanField(
        label="Quer ter permissão de usuário prime?",
        required=False,
        )

    class Meta:
        model = CustomUser
        fields = ("username", "email",)
        field_classes = {"username": UsernameField}