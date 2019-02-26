from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class CollectionUser(models.Model):
    collection = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        verbose_name=_('collection id'),
        help_text=_('Collection to which user belongs'),
        on_delete=models.CASCADE,
        blank=False)
    user = models.ForeignKey(
        User,
        db_column='user_id',
        verbose_name=_('user id'),
        help_text=_('User of collection'),
        on_delete=models.CASCADE,
        blank=False)
    role = models.ForeignKey(
        'CollectionRole',
        on_delete=models.PROTECT,
        db_column='role',
        verbose_name=_('role'),
        help_text=_('Role of user in collection'),
        blank=False)
    metadata_type = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        db_column='metadata_type',
        verbose_name=_('metadata type'),
        help_text=_('JSON schema for collection user metadata'),
        limit_choices_to=(
            models.Q(field__exact='collection_user_metadata') |
            models.Q(field__exact='global')),
        to_field='name',
        default='free',
        blank=False,
        null=False)
    metadata = JSONField(
        blank=True,
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to user in collection'),
        null=True)

    class Meta:
        verbose_name = _('Collection User')
        verbose_name_plural = _('Collection Users')

    def __str__(self):
        msg = _('User {user} of collection {collection}').format(
            user=str(self.user),
            collection=str(self.collection))
        return msg
