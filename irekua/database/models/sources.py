from django.db import models
from django.contrib.auth.models import User


class Source(models.Model):
    directory = models.CharField(
        max_length=64,
        blank=False)
    source_file = models.CharField(
        max_length=64,
        blank=False)
    parse_function = models.CharField(
        max_length=50,
        blank=False)
    uploaded_on = models.DateTimeField(
        auto_now_add=True)
    uploader = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='source_uploader',
        blank=False)
