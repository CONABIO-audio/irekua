from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from database.utils import validate_json_instance


class Collection(models.Model):
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
    metadata_type = models.ForeignKey(
        'Schema',
        related_name='collection_metadata_type',
        on_delete=models.PROTECT,
        db_column='metadata_type',
        verbose_name=_('metadata type'),
        help_text=_('JSON schema for collection metadata'),
        limit_choices_to=(
            models.Q(field__exact='collection_metadata') |
            models.Q(field__exact='global')),
        to_field='name',
        default='free',
        blank=False,
        null=False)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Collection metadata'),
        blank=True,
        null=True)
    coordinator = models.ForeignKey(
        User,
        related_name='collection_coordinator',
        on_delete=models.PROTECT,
        db_column='coordinator_id',
        verbose_name=_('coordinator id'),
        help_text=_('Collection coordinator'),
        blank=True,
        null=True)
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

    schemas = models.ManyToManyField(
        'Schema',
        related_name='collection_schemas',
        through='CollectionSchema',
        through_fields=('collection', 'schema'))
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

    def clean(self, *args, **kwargs):
        validate_json_instance(self.metadata, self.metadata_type.schema)
        super(Collection, self).clean(*args, **kwargs)
