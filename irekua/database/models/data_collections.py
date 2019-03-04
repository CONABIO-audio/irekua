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

    roles = models.ManyToManyField(
        'RoleType',
        through='CollectionRole',
        through_fields=('collection', 'role_type'))
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

    def validate_site(self, site):
        self.collection_type.validate_site(site)

    def validate_site_metadata(self, metadata):
        self.collection_type.validate_site_metadata(metadata)

    def has_user(self, user):
        try:
            self.users.get(username=user.username)
            return True
        except self.users.model.DoesNotExist:
            return False
