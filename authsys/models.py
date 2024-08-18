from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Dummy(models.Model):
    dummy_field = models.CharField(max_length=50, default="dummy")

    class Meta:
        app_label = "dummy"


class CustomUser(AbstractUser):
    email_validated = models.BooleanField(
        "Campo que define se o email de um usuário foi validado",
        "email_validated",
        blank=True,
        default=False,
    )
