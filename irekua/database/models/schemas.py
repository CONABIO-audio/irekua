from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import jsonschema


from database.utils import (
    empty_json,
    FREE_SCHEMA
)


def not_reserved_names(value):
    if value == Schema.FREE_SCHEMA:
        raise ValidationError(
            _('%(value)s is a reserved schema name'),
            params={'value': value})

def validate_json_schema(schema):
    try:
        jsonschema.validate(schema=schema, instance={})
    except jsonschema.exceptions.SchemaError as error:
        msg = _('JSON Schema is not valid. Error: %(error)s')
        params = dict(error=str(error))
        raise ValidationError(msg, params=params)
    except jsonschema.exceptions.ValidationError:
        pass


def validate_json_instance(schema, instance):
    try:
        jsonschema.validate(schema=schema, instance=instance)
    except jsonschema.exceptions.ValidationError as error:
        msg = _('Instance does not comply with JSON schema. Error: %(error)s')
        params = dict(error=str(error))
        raise ValidationError(msg, params=params)

class Schema(models.Model):
    FREE_SCHEMA = FREE_SCHEMA

    ANNOTATION = 'annotation'
    ANNOTATION_CONFIGURATION = 'annotation_configuration'
    ANNOTATION_METADATA = 'annotation_metadata'
    COLLECTION_METADATA = 'collection_metadata'
    COLLECTION_DEVICE_METADATA = 'collection_device_metadata'
    COLLECTION_SITE_METADATA = 'collection_site_metadata'
    COLLECTION_USER_METADATA = 'collection_user_metadata'
    DEVICE_METADATA = 'device_metadata'
    DEVICE_CONFIGURATION = 'device_configuration'
    ENTAILMENT_METADATA = 'entailment_metadata'
    ITEM_MEDIA_INFO = 'item_media_info'
    ITEM_METADATA = 'item_metadata'
    LICENCE_METADATA = 'licence_metadata'
    SAMPLING_EVENT_METADATA = 'sampling_event_metadata'
    SECONDARY_ITEM_MEDIA_INFO = 'secondary_item_media_info'
    SITE_METADATA = 'site_metadata'
    SYNONYM_METADATA = 'synonym_metadata'
    TERM_METADATA = 'term_metadata'
    GLOBAL = 'global'
    JSON_FIELDS = [
        (ANNOTATION, _('annotation')),
        (ANNOTATION_CONFIGURATION, _('annotation configuration')),
        (ANNOTATION_METADATA, _('annotation metadata')),
        (COLLECTION_METADATA, _('collection metadata')),
        (COLLECTION_DEVICE_METADATA, _('collection device metadata')),
        (COLLECTION_SITE_METADATA, _('collection site metadata')),
        (COLLECTION_USER_METADATA, _('collection user metadata')),
        (DEVICE_METADATA, _('device metadata')),
        (DEVICE_CONFIGURATION, _('device configuration')),
        (ENTAILMENT_METADATA, _('entailment metadata')),
        (ITEM_MEDIA_INFO, _('item media info')),
        (ITEM_METADATA, _('item metadata')),
        (LICENCE_METADATA, _('licence metadata')),
        (SAMPLING_EVENT_METADATA, _('sampling event metadata')),
        (SECONDARY_ITEM_MEDIA_INFO, _('secondary item media info')),
        (SITE_METADATA, _('site metadata')),
        (SYNONYM_METADATA, _('synonym metadata')),
        (TERM_METADATA, _('term metadata')),
        (GLOBAL, _('global')),
    ]

    field = models.CharField(
        max_length=64,
        blank=False,
        db_column='field',
        verbose_name=_('field'),
        help_text=_('Field to which JSON schema applies'),
        null=False,
        choices=JSON_FIELDS)
    name = models.CharField(
        max_length=64,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of JSON schema'),
        validators=[not_reserved_names],
        unique=True,
        blank=False,
        null=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of schema'),
        blank=True)
    schema = JSONField(
        blank=False,
        db_column='schema',
        verbose_name=_('schema'),
        help_text=_('JSON object with schema'),
        default=empty_json,
        null=False)

    class Meta:
        verbose_name = _('Schema')
        verbose_name_plural = _('Schemas')
        unique_together = (('field', 'name'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
    def clean(self):
        try:
            validate_json_schema(self.schema)
        except ValidationError as error:
            raise ValidationError({'schema': error})
        super(Schema, self).clean()

    def validate_instance(self, instance):
        validate_json_instance(self.schema, instance)
