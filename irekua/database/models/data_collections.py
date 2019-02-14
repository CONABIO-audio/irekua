from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Collection(models.Model):
    name = models.CharField(
        max_length=70,
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
        help_text=_('Collection metadata'),
        blank=False)
    coordinator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        db_column='coordinator_id',
        verbose_name=_('coordinator id'),
        help_text=_('Collection coordinator'),
        blank=True,
        null=True)


class CollectionOwner(models.Model):
    collection = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        verbose_name=_('collection id'),
        help_text=_('Collection beign owned'),
        on_delete=models.CASCADE,
        blank=False)
    user = models.ForeignKey(
        User,
        db_column='user_id',
        verbose_name=_('user id'),
        help_text=_('User owner of collection'),
        on_delete=models.CASCADE,
        blank=False)
