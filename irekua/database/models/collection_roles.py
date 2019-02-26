from django.db import models
from django.utils.translation import gettext_lazy as _


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

    class Meta:
        verbose_name = _('Collection Role')
        verbose_name_plural = _('Collection Roles')

    def __str__(self):
        msg = _('Role {role} for collection {collection}').format(
            role=str(self.role),
            collection=str(self.collection))
        return msg
