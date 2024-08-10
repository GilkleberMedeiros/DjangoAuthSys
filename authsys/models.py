from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Dummy(models.Model):
    dummy_field = models.CharField(max_length=50, default="dummy")

    class Meta:
        app_label = "dummy"
