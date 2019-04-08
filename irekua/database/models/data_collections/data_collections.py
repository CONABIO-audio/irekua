from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from database.utils import empty_JSON

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

    physical_devices = models.ManyToManyField(
        'PhysicalDevice',
        through='CollectionDevice',
        through_fields=('collection', 'physical_device'),
        blank=True)
    sites = models.ManyToManyField(
        'Site',
        through='CollectionSite',
        through_fields=('collection', 'site'),
        blank=True)
    users = models.ManyToManyField(
        'User',
        related_name='collection_users',
        through='CollectionUser',
        through_fields=('collection', 'user'),
        blank=True)
    administrators = models.ManyToManyField(
        'User',
        related_name='collection_administrators',
        verbose_name=_('administrators'),
        help_text=_('Administrators of collection'),
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
        verbose_name = _('Collection')
        verbose_name_plural = _('Collections')

        permissions = (
            (
                "add_collection_site",
                _("Can add site to collection")),
            (
                "add_collection_item",
                _("Can add item to collection")),
            (
                "add_collection_device",
                _("Can add device to collection")),
            (
                "add_collection_user",
                _("Can add user to collection")),
            (
                "add_collection_licence",
                _("Can add licence to collection")),
            (
                "add_collection_annotation",
                _("Can annotate items in collection")),
            (
                "add_collection_annotation_vote",
                _("Can vote on annotations of items in collection")),
            (
                "view_collection_sites",
                _("Can view sites in collection")),
            (
                "view_collection_items",
                _("Can view items in collection")),
            (
                "view_collection_devices",
                _("Can view devices in collection")),
            (
                "view_collection_sampling_events",
                _("Can view sampling event in collection")),
            (
                "view_collection_annotations",
                _("Can view annotations of items in collection")),
            (
                "change_collection_sites",
                _("Can change sites in collection")),
            (
                "change_collection_users",
                _("Can change user info in collection")),
            (
                "change_collection_items",
                _("Can change items in collection")),
            (
                "change_collection_devices",
                _("Can change devices in collection")),
            (
                "change_collection_annotations",
                _("Can change annotations of items in collection")),
            (
                "change_collection_sampling_events",
                _("Can change sampling events in collection")),
            (
                "download_collection_items",
                _("Can download annotation items")),
        )

        ordering = ['name']

    def __str__(self):
        return self.name

    def clean(self):
        try:
            self.collection_type.validate_metadata(self.metadata)
        except ValidationError as error:
            msg = _(
                'Invalid metadata for collection of type {type}. '
                'Error: {error}')
            msg = msg.format(
                type=str(self.collection_type),
                error=str(error))
            raise ValidationError({'metadata': msg})
        super(Collection, self).clean()

    def add_user(self, user, role, metadata, is_admin=False):
        CollectionUser.objects.create(
            collection=self,
            user=user,
            role=role,
            metadata=metadata,
            is_admin=is_admin)

    def add_site(self, site, internal_id, metadata):
        CollectionSite.objects.create(
            collection=self,
            site=site,
            internal_id=internal_id,
            metadata=metadata)

    def add_device(self, physical_device, internal_id, metadata):
        CollectionDevice.objects.create(
            collection=self,
            physical_device=physical_device,
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
        return self.collection_type.validate_and_get_licence_type(licence_type)

    def validate_and_get_role(self, role):
        return self.collection_type.validate_and_get_role(role)

    def validate_and_get_licence(self, licence):
        try:
            licence = self.licence_set.get(pk=licence.pk)
        except self.licences.model.DoesNotExist:
            msg = _(
                'Licence %(licence)s is not part of collection '
                '%(collection)s.')
            params = dict(
                licence=str(licence),
                collection=str(self))
            raise ValidationError(msg, params=params)

    def is_admin(self, user):
        queryset = self.administrators.filter(user=user)
        return queryset.exists()

    def has_user(self, user):
        return CollectionUser.objects.filter(
            collection=self,
            user=user).exists()

    def has_permission(self, user, codename):
        try:
            collectionuser = CollectionUser.objects.get(
                collection=self,
                user=user)
            role = collectionuser.role
        except CollectionUser.DoesNotExist:
            return False

        return role.has_permission(codename)
