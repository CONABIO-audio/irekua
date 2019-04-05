from django.db import models
from django.utils.translation import gettext_lazy as _


class DeviceBrand(models.Model):
    name = models.CharField(
        max_length=128,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of device brand'),
        primary_key=True,
        blank=False)
    website = models.URLField(
        db_column='website',
        verbose_name=_('website'),
        help_text=_('Brand\'s website'),
        blank=True,
        null=True)
    logo = models.ImageField(
        db_column='logo',
        verbose_name=_('logo'),
        help_text=_('Logo of device brand'),
        upload_to='images/device_brands/',
        blank=True,
        null=True)

    created_on = models.DateTimeField(
        db_column='created_on',
        verbose_name=_('created on'),
        help_text=_('Date of entry creation'),
        auto_now_add=True,
        editable=False)
    modified_on = models.DateTimeField(
        db_column='modified_on',
        verbose_name=_('modified on'),
        help_text=_('Date of last modification'),
        auto_now=True,
        editable=False)

    class Meta:
        verbose_name = _('Device Brand')
        verbose_name_plural = _('Device Brands')

        ordering = ['name']

    def __str__(self):
        return self.name
