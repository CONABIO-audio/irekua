from django.contrib.postgres.fields import JSONField
from django.db import models


class SecondaryItem(models.Model):
    HASH_FUNCTIONS = [
        ('md5', 'md5'),
        ('sha244', 'sha244'),
        ('sha256', 'sha256'),
        ('sha384', 'sha384'),
        ('sha512', 'sha512'),
    ]

    path = models.CharField(
        max_length=70,
        blank=False)
    hash = models.CharField(
        max_length=64,
        blank=False)
    hash_function = models.CharField(
        max_length=10,
        blank=False,
        choices=HASH_FUNCTIONS)
    created_on = models.DateTimeField(
        auto_now_add=True)
    type = models.CharField(
        max_length=40,
        blank=False)
    item = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
        blank=False)
    media_info = JSONField(
        blank=False)
