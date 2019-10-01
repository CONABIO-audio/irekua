from django.db import models
from django.utils.translation import gettext_lazy as _


class Locality(models.Model):
    name = models.CharField(
        max_length=128,
        db_column='name',
        help_text=_('Name of locality'))

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

        ordering = ['-name']
