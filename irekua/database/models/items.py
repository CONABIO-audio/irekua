from django.contrib.postgres.fields import JSONField, ArrayField
from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
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
    filesize = models.IntegerField(
        blank=False)
    hash = models.CharField(
        max_length=64,
        blank=False)
    hash_function = models.CharField(
        max_length=10,
        blank=False,
        choices=HASH_FUNCTIONS)
    type = models.CharField(
        max_length=40,
        blank=False)
    source_foreign_key = models.CharField(
        max_length=50,
        blank=True)
    media_info = JSONField(
        blank=False)
    sampling = models.ForeignKey(
        'SamplingEvent',
        blank=True,
        null=True)
    source = models.ForeignKey(
        'Source',
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    metadata = JSONField(
        blank=True,
        null=True)
    keywords = ArrayField(
        models.CharField(
            max_length=30))
    captured_on = models.DateTimeField(
        blank=False)
    created_on = models.DateTimeField(
        auto_now_add=True)
    collection = models.ForeignKey(
        'Collection',
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    owner = models.ForeignKey(
        User,
        related_name='owner',
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    licence = models.ForeignKey(
        'Licence',
        on_delete=models.PROTECT,
        blank=False)
