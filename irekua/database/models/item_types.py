import mimetypes
from django.db import models
from django.utils.translation import gettext_lazy as _

from database.models.schemas import Schema


mimetypes.init()


class ItemType(models.Model):
    MIME_TYPES = [
        (value, value) for value in
        sorted(list(set(mimetypes.types_map.values())))
    ]

    name = models.CharField(
        max_length=64,
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
        limit_choices_to={'field': Schema.ITEM_MEDIA_INFO},
        help_text=_('Reference to JSON Schema to be used with media info of this item type'),
        blank=False,
        null=False)
    media_type = models.CharField(
        max_length=128,
        db_column='media_type',
        verbose_name=_('media type'),
        help_text=_('MIME type associated with item type'),
        blank=False,
        choices=MIME_TYPES)
    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Item type icon'),
        upload_to='images/item_types/',
        blank=True,
        null=True)

    event_types = models.ManyToManyField(
        'EventType',
        db_column='event_types',
        verbose_name=_('event types'),
        help_text=_('Types of event for this item type'))

    class Meta:
        verbose_name = _('Item Type')
        verbose_name_plural = _('Item Types')

    def __str__(self):
        return self.name

    class InvalidEventType(Exception):
        pass

    def validate_event_type(self, event_type):
        try:
            self.event_types.get(name=event_type.name)
        except self.event_types.model.DoesNotExist:
            raise self.InvalidEventType
