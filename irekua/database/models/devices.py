from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Device(models.Model):
    serial_number = models.CharField(
        max_length=100,
        db_column='serial_number',
        verbose_name=_('serial number'),
        help_text=_('Serial number of device'),
        blank=True,
        null=True,
        unique=True)
    type = models.CharField(
        max_length=50,
        db_column='type',
        verbose_name=_('type'),
        help_text=_('Type of device'),
        blank=False)
    brand = models.CharField(
        max_length=50,
        db_column='brand',
        verbose_name=_('brand'),
        help_text=_('Brand of device'),
        blank=False)
    model = models.CharField(
        max_length=50,
        db_column='model',
        verbose_name=_('model'),
        help_text=_('Model of device'),
        blank=False)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        db_column='owner_id',
        verbose_name=_('owner'),
        help_text=_('Owner of device'),
        null=True,
        blank=True)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to device'),
        null=True,
        blank=True)
    bundle = models.BooleanField(
        db_column='bundle',
        verbose_name=_('bundle'),
        help_text=_('Does this device possibly represents many physical devices?'),
        blank=False)
