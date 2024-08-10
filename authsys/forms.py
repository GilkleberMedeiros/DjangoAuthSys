from django.forms import Form, ModelForm, BooleanField

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField


class UserSignUpModelForm(UserCreationForm):
    prime_user_permission = BooleanField(
        label="Quer ter permissão de usuário prime?",
        required=False,
        )

    class Meta:
        model = User
        fields = ("username", "email",)
        field_classes = {"username": UsernameField}