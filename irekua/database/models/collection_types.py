from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

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
        verbose_name=_('metadata schema'),
        help_text=_('JSON Schema to be used with collection metadata for collections of this type'),
        limit_choices_to=(
            models.Q(field__exact=Schema.COLLECTION_METADATA) |
            models.Q(field__exact=Schema.GLOBAL)),
        to_field='name',
        default=Schema.FREE_SCHEMA,
        blank=False,
        null=False)

    anyone_can_create = models.BooleanField(
        db_column='anyone_can_create',
        verbose_name=_('anyone can create'),
        help_text=_('Boolean flag indicating wheter any user can create collections of this type'),
        blank=True,
        default=False,
        null=False
    )
    administrators = models.ManyToManyField(
        User,
        verbose_name=_('administrators'),
        help_text=_('Administrators of this collection type. Administrators can create collections of this type'),
        blank=True)

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
    restrict_sampling_event_types = models.BooleanField(
        db_column='restrict_sampling_event_types',
        verbose_name=_('restrict sampling event types'),
        help_text=_('Flag indicating whether types of sampling events are restricted to registered ones'))

    site_types = models.ManyToManyField(
        'SiteType',
        db_column='site_types',
        verbose_name=_('site types'),
        help_text=_('Types of sites valid for collections of type'),
        blank=True)
    annotation_types = models.ManyToManyField(
        'AnnotationType',
        db_column='annotation_types',
        verbose_name=_('annotation types'),
        help_text=_('Types of annotations valid for collections of type'),
        blank=True)
    licence_types = models.ManyToManyField(
        'LicenceType',
        db_column='licence_types',
        verbose_name=_('licence types'),
        help_text=_('Types of licences valid for collections of type'),
        blank=True)
    event_types = models.ManyToManyField(
        'EventType',
        db_column='event_types',
        verbose_name=_('event types'),
        help_text=_('Types of events valid for collections of type'),
        blank=True)
    sampling_event_types = models.ManyToManyField(
        'SamplingEventType',
        db_column='sampling_event_types',
        verbose_name=_('sampling event types'),
        help_text=_('Types of sampling events valid for collections of type'),
        blank=True)
    item_types = models.ManyToManyField(
        'ItemType',
        through='CollectionItemType',
        through_fields=('collection_type', 'item_type'),
        db_column='item_types',
        verbose_name=_('item types'),
        help_text=_('Types of items valid for collections of type'),
        blank=True)
    device_types = models.ManyToManyField(
        'DeviceType',
        through='CollectionDeviceType',
        through_fields=('collection_type', 'device_type'),
        db_column='device_types',
        verbose_name=_('device types'),
        help_text=_('Types of devices valid for collections of type'),
        blank=True)
    role_types = models.ManyToManyField(
        'RoleType',
        through='CollectionRoleType',
        through_fields=('collection_type', 'role_type'),
        db_column='role_types',
        verbose_name=_('role types'),
        help_text=_('Types of roles valid for collections of type'),
        blank=True)

    class Meta:
        verbose_name = _('Collection Type')
        verbose_name_plural = _('Collection Types')

    def __str__(self):
        return self.name

    def validate_metadata(self, metadata):
        try:
            self.metadata_schema.validate_instance(metadata)
        except ValidationError as error:
            msg = _('Invalid collection metadata for collection of type %(type)s. Error: %(error)s')
            params = dict(type=str(self), error=str(error))
            raise ValidationError(msg, params=params)

    def validate_and_get_site_type(self, site_type):
        if not self.restrict_site_types:
            return

        try:
            return self.site_types.get(name=site_type)
        except self.site_types.model.DoesNotExist:
            msg = _('Site type %(site_type)s is not accepted in collection of type %(col_type)s or does not exist')
            params = dict(
                site_type=site_type,
                col_type=str(self))
            raise ValidationError(msg, params=params)

    def validate_and_get_annotation_type(self, annotation_type):
        if not self.restrict_annotation_types:
            return

        try:
            return self.annotation_types.get(name=annotation_type)
        except self.annotation_types.model.DoesNotExist:
            msg = _('Annotation type %(annotation_type)s is not accepted in collection of type %(col_type)s or does not exist')
            params = dict(
                annotation_type=annotation_type,
                col_type=str(self))
            raise ValidationError(msg, params=params)

    def validate_and_get_licence_type(self, licence_type):
        if not self.restrict_licence_types:
            return

        try:
            return self.licence_type.get(name=licence_type)
        except self.licence_types.model.DoesNotExist:
            msg = _('Licence type %(licence_type)s is not accepted in collection of type %(col_type)s or does not exist')
            params = dict(
                licence_type=licence_type,
                col_type=str(self))
            raise ValidationError(msg, params=params)

    def validate_and_get_event_type(self, event_type):
        if not self.restrict_event_types:
            return

        try:
            return self.event_types.get(name=event_type)
        except self.event_types.model.DoesNotExist:
            msg = _('Event type %(event_type)s is not accepted in collection of type %(col_type)s or does not exist')
            params = dict(
                event_type=event_type,
                col_type=str(self))
            raise ValidationError(msg, params=params)

    def validate_and_get_item_type(self, item_type):
        if not self.restrict_item_types:
            return

        try:
            return self.item_types.get(name=item_type)
        except self.item_types.model.DoesNotExist:
            msg = _('Item type %(item_type)s is not accepted in collection of type %(col_type)s or does not exist')
            params = dict(
                item_type=item_type,
                col_type=str(self))
            raise ValidationError(msg, params=params)

    def validate_and_get_device_type(self, device_type):
        if not self.restrict_device_types:
            return

        try:
            return self.device_types.get(name=device_type)
        except self.device_types.model.DoesNotExist:
            msg = _('Item type %(device_type)s is not accepted in collection of type %(col_type)s or does not exist')
            params = dict(
                device_type=device_type,
                col_type=str(self))
            raise ValidationError(msg, params=params)

    def validate_and_get_sampling_event_type(self, sampling_event_type):
        if not self.restrict_sampling_event_types:
            return

        try:
            return self.sampling_event_types.get(name=sampling_event_type)
        except self.sampling_event_types.model.DoesNotExist:
            msg = _('Sampling Event type %(sampling_event_type)s is not accepted in collection of type %(col_type)s or does not exist')
            params = dict(
                sampling_event_type=sampling_event_type,
                col_type=str(self))
            raise ValidationError(msg, params=params)
