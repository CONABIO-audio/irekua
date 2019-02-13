from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db import models


class UserData(models.Model):
    USER_ROLES = [
        ('admin', 'admin'),
        ('developer', 'developer'),
        ('curator', 'curator'),
        ('user', 'user')
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=False)
    organization = models.CharField(
        max_length=50,
        blank=False)
    role = models.CharField(
        max_length=30,
        choices=USER_ROLES,
        blank=False)
    metadata = JSONField(
        blank=True,
        null=True)
