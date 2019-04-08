from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class MetaCollection(models.Model):
    name = models.CharField(
        max_length=64,
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

    items = models.ManyToManyField(
        'Item',
        verbose_name=_('items'),
        help_text=_('Items belonging to MetaCollection'),
        blank=True)
    curators = models.ManyToManyField(
        'User',
        related_name='metacollection_curators',
        verbose_name='curators',
        help_text=_('Curators of metacollection'),
        blank=True)

    created_by = models.ForeignKey(
        'User',
        related_name='metacollection_created_by',
        on_delete=models.CASCADE,
        db_column='created_by',
        verbose_name=_('created by'),
        help_text=_('Creator of Meta Collection'),
        null=True,
        blank=True)
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
        verbose_name = _('Meta Collection')
        verbose_name_plural = _('Meta Collections')

        ordering = ['name']

    def __str__(self):
        return self.name

    def add_item(self, item):
        self.items.add(item)
        self.save()

    def remove_item(self, item):
        self.items.remove(item)
        self.save()

    def add_curator(self, user):
        self.curators.add(user)
        self.save()

    def remove_curator(self, user):
        self.curators.remove(user)
        self.save()
