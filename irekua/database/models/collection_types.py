from django.db import models
from django.utils.translation import gettext_lazy as _

from database.models.schemas import Schema


class CollectionType(models.Model):
    name = models.CharField(
        max_length=128,
        primary_key=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of collection type'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of collection type'),
        blank=False)
    metadata_schema = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        db_column='metadata_schema_id',
        verbose_name=_('metadata schema id'),
        help_text=_('JSON Schema to be used with collection metadata for collections of this type'),
        limit_choices_to=(
            models.Q(field__exact=Schema.COLLECTION_METADATA) |
            models.Q(field__exact=Schema.GLOBAL)),
        to_field='name',
        default=Schema.FREE_SCHEMA,
        blank=False,
        null=False)

    restrict_site_types = models.BooleanField(
        db_column='restrict_site_types',
        verbose_name=_('restrict site types'),
        help_text=_('Flag indicating whether types of sites are restricted to registered ones'))
    restrict_annotation_types = models.BooleanField(
        db_column='restrict_annotation_types',
        verbose_name=_('restrict annotation types'),
        help_text=_('Flag indicating whether types of annotations are restricted to registered ones'))
    restrict_item_types = models.BooleanField(
        db_column='restrict_item_types',
        verbose_name=_('restrict item types'),
        help_text=_('Flag indicating whether types of items are restricted to registered ones'))
    restrict_licence_types = models.BooleanField(
        db_column='restrict_licence_types',
        verbose_name=_('restrict licence types'),
        help_text=_('Flag indicating whether types of licences are restricted to registered ones'))
    restrict_device_types = models.BooleanField(
        db_column='restrict_device_types',
        verbose_name=_('restrict device types'),
        help_text=_('Flag indicating whether types of devices are restricted to registered ones'))
    restrict_event_types = models.BooleanField(
        db_column='restrict_event_types',
        verbose_name=_('restrict event types'),
        help_text=_('Flag indicating whether types of events are restricted to registered ones'))

    site_types = models.ManyToManyField(
        'SiteType')
    annotation_types = models.ManyToManyField(
        'AnnotationType')
    licence_types = models.ManyToManyField(
        'LicenceType')
    event_types = models.ManyToManyField(
        'EventType')
    item_types = models.ManyToManyField(
        'ItemType',
        through='CollectionItemType',
        through_fields=('collection', 'item_type'))
    device_types = models.ManyToManyField(
        'DeviceType',
        through='CollectionDeviceType',
        through_fields=('collection', 'device_type'))

    class Meta:
        verbose_name = _('Collection Type')
        verbose_name_plural = _('Collection Types')

    def __str__(self):
        return self.name
