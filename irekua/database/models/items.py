from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from database.models.schemas import Schema
from database.utils import (
    validate_json_instance,
    validate_is_of_collection,
    empty_json,
)


class Item(models.Model):
    HASH_FUNCTIONS = [
        ('md5', 'md5'),
        ('sha244', 'sha244'),
        ('sha256', 'sha256'),
        ('sha384', 'sha384'),
        ('sha512', 'sha512'),
    ]

    path = models.CharField(
        max_length=70,
        db_column='path',
        verbose_name=_('path'),
        unique=True,
        help_text=_('Path to resource'),
        blank=False)
    filesize = models.IntegerField(
        db_column='filesize',
        verbose_name=_('file size'),
        help_text=_('Size of resouce in Bytes'),
        blank=False)
    hash = models.CharField(
        db_column='hash',
        verbose_name=_('hash'),
        help_text=_('Hash of resource file'),
        max_length=64,
        unique=True,
        blank=False)
    hash_function = models.CharField(
        db_column='hash_function',
        verbose_name=_('hash function'),
        help_text=_('Function used to create hash of file'),
        max_length=10,
        blank=False,
        choices=HASH_FUNCTIONS)
    item_type = models.ForeignKey(
        'ItemType',
        on_delete=models.PROTECT,
        db_column='item_type',
        verbose_name=_('item type'),
        help_text=_('Type of resource'),
        blank=False)
    source_foreign_key = models.CharField(
        db_column='source_foreign_key',
        verbose_name=_('source foreign key'),
        help_text=_('Foreign key of file in source database'),
        max_length=50,
        blank=True)
    media_info = JSONField(
        db_column='media_info',
        default=empty_json,
        verbose_name=_('media info'),
        help_text=_('Information of resource file'),
        blank=False)
    sampling = models.ForeignKey(
        'SamplingEvent',
        db_column='sampling_id',
        verbose_name=_('sampling id'),
        help_text=_('Sampling event associated with item'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    source = models.ForeignKey(
        'Source',
        db_column='event_id',
        verbose_name=_('event id'),
        help_text=_('Reference to source of item (parsing function and parent directory)'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    metadata_type = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        db_column='metadata_type',
        verbose_name=_('metadata type'),
        help_text=_('Schema for item metadata structure'),
        limit_choices_to=(
            models.Q(field__exact=Schema.ITEM_METADATA) |
            models.Q(field__exact=Schema.GLOBAL)),
        to_field='name',
        default=Schema.FREE_SCHEMA,
        blank=False,
        null=False)
    metadata = JSONField(
        db_column='metadata',
        default=empty_json,
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to item'),
        blank=True,
        null=True)
    captured_on = models.DateTimeField(
        db_column='captured_on',
        verbose_name=_('captured on'),
        help_text=_('Date on which item was produced'),
        blank=False)
    created_on = models.DateTimeField(
        db_column='created_on',
        verbose_name=_('created on'),
        help_text=_('Date on which item was uploaded to database'),
        auto_now_add=True)
    collection = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        verbose_name=_('collection id'),
        help_text=_('Collection to which item belongs'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    owner = models.ForeignKey(
        User,
        db_column='owner_id',
        verbose_name=_('owner id'),
        help_text=_('Owner of item'),
        related_name='owner',
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    licence = models.ForeignKey(
        'Licence',
        db_column='licence',
        verbose_name=_('licence'),
        help_text=_('Licence of item'),
        on_delete=models.PROTECT,
        blank=False)
    is_uploaded = models.BooleanField(
        blank=False,
        null=False,
        db_column='is_uploaded',
        verbose_name=_('is uploaded'),
        help_text=_('Is the item file on the server?'))

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')

        permissions = (
            ("download_item", _("Can download item")),
        )

    def __str__(self):
        return 'Item {id}'.format(id=self.id)

    def clean(self, *args, **kwargs):
        validate_json_instance(
            self.media_info,
            self.item_type.media_info_schema.schema)
        validate_json_instance(
            self.metadata,
            self.metadata_type.schema)
        validate_is_of_collection(
            self.collection,
            self.metadata_type)
        super(Item, self).clean(*args, **kwargs)

    def validate_annotation(self, annotation):
        self.item_type.validate_event_type(annotation.event_type)
        self.collection.validate_annotation_type(annotation.annotation_type)
