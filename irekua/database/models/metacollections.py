from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class MetaCollection(models.Model):
    name = models.CharField(
        max_length=50,
        primary_key=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of meta collection'),
        null=False,
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of Meta Collection'),
        blank=False)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='creator_id',
        verbose_name=_('creator'),
        help_text=_('Reference to creator of Meta Collection'),
        null=True,
        blank=True)
    items = models.ManyToManyField(
        'Item',
        db_column='items',
        verbose_name=_('items'),
        help_text=_('Items belonging to MetaCollection'))

    class Meta:
        verbose_name = _('Meta Collection')
        verbose_name_plural = _('Meta Collections')

    def __str__(self):
        return self.name
