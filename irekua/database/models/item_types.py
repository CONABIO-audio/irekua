import mimetypes
from django.db import models
from django.core.exceptions import ValidationError
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
        verbose_name=_('media info schema'),
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
        help_text=_('Types of event for this item type'),
        blank=True)

    class Meta:
        verbose_name = _('Item Type')
        verbose_name_plural = _('Item Types')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
    def validate_media_info(self, media_info):
        try:
            self.media_info_schema.validate_instance(media_info)
        except ValidationError as error:
            msg = _('Invalid media info for item of type %(type)s. Error %(error)s')
            params = dict(type=str(self), error=str(error))
            raise ValidationError(msg, params=params)

    def validate_and_get_event_type(self, event_type):
        try:
            return self.event_types.get(name=event_type.name)
        except self.event_types.model.DoesNotExist:
            msg = _('Event type %(event_type)s is invalid for item type %(item_type)s')
            params = dict(even_type=str(event_type), item_type=str(self))
            raise ValidationError(msg, params=params)
