from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from database.utils import (
    GENERIC_COLLECTION,
    empty_JSON,
)

from .collection_licences import CollectionLicence
from .collection_users import CollectionUser
from .collection_devices import CollectionDevice
from .collection_sites import CollectionSite


class Collection(models.Model):
    collection_type = models.ForeignKey(
        'CollectionType',
        on_delete=models.PROTECT,
        db_column='collection_type_id',
        verbose_name=_('collection type'),
        help_text=_('Type of collection'),
        default=GENERIC_COLLECTION,
        to_field='name',
        blank=False,
        null=False)
    name = models.CharField(
        max_length=128,
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
        blank=True,
        default=empty_JSON,
        null=False)
    institution = models.ForeignKey(
        'Institution',
        on_delete=models.PROTECT,
        db_column='institution_id',
        verbose_name=_('institution'),
        help_text=_('Institution to which the collection belogs'),
        blank=True,
        null=True)
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
        through_fields=('collection', 'device'),
        blank=True)
    sites = models.ManyToManyField(
        'Site',
        through='CollectionSite',
        through_fields=('collection', 'site'),
        blank=True)
    users = models.ManyToManyField(
        User,
        related_name='collection_users',
        through='CollectionUser',
        through_fields=('collection', 'user'),
        blank=True)
    licences = models.ManyToManyField(
        'Licence',
        through='CollectionLicence',
        through_fields=('collection', 'licence'),
        verbose_name=_('licences'),
        help_text=_('Signed licences for items in this collection'),
        blank=True)

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
        super(Collection, self).clean()

    def add_licence(self, licence):
        CollectionLicence.objects.create(collection=self, licence=licence)

    def add_user(self, user, role, metadata, is_admin=False):
        CollectionUser.objects.create(
            collection=self,
            user=user,
            role=role,
            metadata=metadata,
            is_admin=is_admin)

    def add_site(self, site, internal_id, metadata):
        CollectionSite.objects.create(
            collection=collection,
            site=site,
            internal_id=internal_id,
            metadata=metadata)

    def add_device(self, device, internal_id, metadata):
        CollectionDevice.objects.create(
            collection=collection,
            device=device,
            internal_id=internal_id,
            metadata=metadata)

    def validate_and_get_annotation_type(self, annotation_type):
        return self.collection_type.validate_and_get_annotation_type(
            annotation_type)

    def validate_and_get_event_type(self, event_type):
        return self.collection_type.validate_and_get_event_type(event_type)

    def validate_and_get_site_type(self, site_type):
        return self.collection_type.validate_and_get_site_type(site_type)

    def validate_and_get_device_type(self, device_type):
        return self.collection_type.validate_and_get_device_type(device_type)

    def validate_and_get_item_type(self, item_type):
        return self.collection_type.validate_and_get_item_type(item_type)

    def validate_and_get_sampling_event_type(self, sampling_event_type):
        return self.collection_type.validate_and_get_sampling_event_type(
            sampling_event_type)

    def validate_and_get_licence_type(self, licence_type):
        return self.collection_type.validate_and_get_site_type(licence_type)

    def validate_and_get_role(self, role):
        return self.collection_type.validate_and_get_role(role)

    def validate_and_get_licence(self, licence):
        try:
            licence = self.licences.get(pk=licence.pk)
        except self.licences.model.DoesNotExist:
            msg = _('Licence %(licence)s is not part of collection %(collection)s.')
            params = dict(
                licence=str(licence),
                collection=str(self))
            raise ValidationError(msg, params=params)
