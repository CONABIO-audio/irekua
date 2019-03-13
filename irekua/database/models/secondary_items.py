from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from database.utils import (
    empty_JSON
)


class SecondaryItem(models.Model):
    HASH_FUNCTIONS = [
        ('md5', 'md5'),
        ('sha244', 'sha244'),
        ('sha256', 'sha256'),
        ('sha384', 'sha384'),
        ('sha512', 'sha512'),
    ]

    path = models.CharField(
        max_length=128,
        db_column='path',
        unique=True,
        verbose_name=_('path'),
        help_text=_('Path to secondary resource'),
        blank=False)
    hash = models.CharField(
        max_length=64,
        unique=True,
        db_column='hash',
        verbose_name=_('hash'),
        help_text=_('Hash of secondary resource file'),
        blank=False)
    hash_function = models.CharField(
        max_length=16,
        blank=False,
        db_column='hash_function',
        verbose_name=_('hash function'),
        help_text=_('Hash function used to generate has of secondary file'),
        choices=HASH_FUNCTIONS)
    created_on = models.DateTimeField(
        editable=False,
        db_column='created_on',
        verbose_name=_('created on'),
        help_text=_('Date of creation of secondary item'),
        auto_now_add=True)
    item_type = models.ForeignKey(
        'ItemType',
        on_delete=models.PROTECT,
        db_column='item_type',
        verbose_name=_('item type'),
        help_text=_('Type of file of secondary item'),
        blank=False,
        null=False)
    item = models.ForeignKey(
        'Item',
        db_column='item_id',
        verbose_name=_('item id'),
        help_text=_('Reference to primary item associated to secondary item'),
        on_delete=models.CASCADE,
        blank=False,
        null=False)
    media_info = JSONField(
        db_column='media_info',
        verbose_name=_('media info'),
        help_text=_('Media information of secondary item file'),
        default=empty_JSON,
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Secondary Item')
        verbose_name_plural = _('Secondary Items')

        ordering = ['created_on']

    def __str__(self):
        msg = _('Secondary Item %(id)s derived from %(itemid)s')
        params = dict(
            id=self.id,
            itemid=str(self.item))
        return msg % params

    def clean(self):
        try:
            self.item_type.validate_media_info(self.media_info)
        except ValidationError as error:
            raise ValidationError({'media_info': error})

        super(SecondaryItem, self).clean()
