from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from database.utils import (
    GENERIC_COLLECTION,
    empty_json,
)


class Collection(models.Model):
    collection_type = models.ForeignKey(
        'CollectionType',
        on_delete=models.PROTECT,
        db_column='collection_type',
        verbose_name=_('collection type'),
        help_text=_('Type of collection'),
        default=GENERIC_COLLECTION,
        blank=False,
        null=False)
    name = models.CharField(
        max_length=70,
        primary_key=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of collection'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of collection'),
        blank=False)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to collection'),
        blank=False,
        default=empty_json,
        null=False)
    institution = models.ForeignKey(
        'Institution',
        on_delete=models.PROTECT,
        db_column='institution_id',
        verbose_name=_('institution id'),
        help_text=_('Institution to which the collection belogs'),
        blank=True,
        null=True)
    is_open = models.BooleanField(
        db_column='is_open',
        verbose_name=_('is open'),
        help_text=_('Any user can enter this collection'),
        blank=False,
        null=False)
    logo = models.ImageField(
        db_column='logo',
        verbose_name=_('logo'),
        help_text=_('Logo of data collection'),
        upload_to='images/collections/',
        blank=True,
        null=True)

    devices = models.ManyToManyField(
        'PhysicalDevice',
        through='CollectionDevice',
        through_fields=('collection', 'device'))
    sites = models.ManyToManyField(
        'Site',
        through='CollectionSite',
        through_fields=('collection', 'site'))
    users = models.ManyToManyField(
        User,
        related_name='collection_users',
        through='CollectionUser',
        through_fields=('collection', 'user'))

    class Meta:
        verbose_name = _('Collection')
        verbose_name_plural = _('Collections')

    def __str__(self):
        return self.name

    def clean(self):
        try:
            self.collection_type.validate_metadata(self.metadata)
        except ValidationError as error:
            msg = _('Invalid metadata for collection of type {type}. Error: {error}')
            msg = msg.format(
                type=str(self.collection_type),
                error=str(error))
            raise ValidationError({'metadata': msg})
        super(Collection, self).save()

    def validate_and_get_device_type_annotation_type(self, annotation_type):
        return self.collection_type.validate_and_get_annotation_type(annotation_type)

    def validate_and_get_event_type(self, event_type):
        return self.collection_type.validate_and_get_event_type(event_type)

    def validate_and_get_site_type(self, site_type):
        return self.collection_type.validate_and_get_site_type(site_type)

    def validate_and_get_device_type(self, device_type):
        return self.collection_type.validate_and_get_device_type(device_type)

    def validate_and_get_item_type(self, item_type):
        return self.collection_type.validate_and_get_item_type(item_type)

    def validate_and_get_sampling_event_type(self, sampling_event_type):
        return self.validate_and_get_sampling_event_type(sampling_event_type)
