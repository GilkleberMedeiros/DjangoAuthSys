from django.forms import Form, ModelForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField


class UserSignUpModelForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email",)
        field_classes = {"username": UsernameField}