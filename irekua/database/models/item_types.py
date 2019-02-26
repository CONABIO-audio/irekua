from django.db import models
from django.utils.translation import gettext_lazy as _


class ItemType(models.Model):
    name = models.CharField(
        max_length=50,
        db_column='name',
        verbose_name=_('name'),
        primary_key=True,
        help_text=_('Name of item type'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of item type'),
        blank=False)
    media_info_schema = models.ForeignKey(
        'Schema',
        on_delete=models.CASCADE,
        db_column='media_info_schema_id',
        verbose_name=_('media info schema id'),
        limit_choices_to={'field': 'item_media_info'},
        help_text=_('Reference to JSON Schema to be used with media info of this item type'),
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Item Type')
        verbose_name_plural = _('Item Types')

    def __str__(self):
        return self.name
