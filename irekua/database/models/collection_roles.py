from django.db import models
from django.utils.translation import gettext_lazy as _

from .schemas import Schema


class CollectionRole(models.Model):
    collection = models.ForeignKey(
        'Collection',
        on_delete=models.CASCADE,
        db_column='collection_id',
        verbose_name=_('collection id'),
        help_text=_('Collection in which role applies'),
        blank=False,
        null=False)
    role_type = models.ForeignKey(
        'RoleType',
        on_delete=models.PROTECT,
        db_column='role_type',
        verbose_name=_('role type'),
        help_text=_('Role to be part of collection'),
        blank=False,
        null=False)
    metadata_schema = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        db_column='metadata_type',
        verbose_name=_('metadata type'),
        help_text=_('JSON schema for collection role metadata'),
        limit_choices_to=(
            models.Q(field__exact=Schema.COLLECTION_USER_METADATA) |
            models.Q(field__exact=Schema.GLOBAL)),
        to_field='name',
        default=Schema.FREE_SCHEMA,
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Collection Role')
        verbose_name_plural = _('Collection Roles')

    def __str__(self):
        msg = _('Role {role} for collection {collection}').format(
            role=str(self.role),
            collection=str(self.collection))
        return msg
