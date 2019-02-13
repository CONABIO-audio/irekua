from django.db import models
from django.contrib.auth.models import User


class Model(models.Model):
    name = models.CharField(
        max_length=50,
        blank=False)
    path = models.CharField(
        max_length=50,
        blank=False)
    version = models.CharField(
        max_length=15,
        blank=False)
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=False)
