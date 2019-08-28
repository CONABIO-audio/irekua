import mimetypes
import os

from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from database.utils import empty_JSON
from database.utils import hash_file
from database.models.base import IrekuaModelBaseUser


mimetypes.init()


def get_item_path(instance, filename):
    path_fmt = os.path.join(
        'items',
        '{collection}',
        '{sampling_event}',
        '{sampling_event_device}',
        '{hash}{ext}')

    extension = mimetypes.guess_extension(
        instance.item_type.media_type)
    sampling_event_device = instance.sampling_event_device
    sampling_event = sampling_event_device.sampling_event
    collection = sampling_event.collection

    instance.item_file.open()
    hash_string = hash_file(instance.item_file)

    path = path_fmt.format(
        collection=collection.pk,
        sampling_event=sampling_event.pk,
        sampling_event_device=sampling_event_device.pk,
        hash=hash_string,
        ext=extension)
    return path


class Item(IrekuaModelBaseUser):
    hash_string = None
    item_size = None

    filesize = models.IntegerField(
        db_column='filesize',
        verbose_name=_('file size'),
        help_text=_('Size of resource in Bytes'),
        blank=True,
        null=True)
    hash = models.CharField(
        db_column='hash',
        verbose_name=_('hash'),
        help_text=_('Hash of resource file'),
        max_length=64,
        unique=True,
        blank=True,
        null=False)
    item_type = models.ForeignKey(
        'ItemType',
        on_delete=models.PROTECT,
        db_column='item_type_id',
        verbose_name=_('item type'),
        help_text=_('Type of resource'),
        blank=False)
    item_file = models.FileField(
        upload_to=get_item_path,
        db_column='item_file',
        verbose_name=_('item file'),
        help_text=_('Upload file associated to file'),
        blank=True,
        null=True)
    media_info = JSONField(
        db_column='media_info',
        default=empty_JSON,
        verbose_name=_('media info'),
        help_text=_('Information of resource file'),
        blank=True,
        null=False)
    sampling_event_device = models.ForeignKey(
        'SamplingEventDevice',
        db_column='sampling_event_device_id',
        verbose_name=_('sampling event device'),
        help_text=_('Sampling event device used to create item'),
        on_delete=models.PROTECT,
        blank=False,
        null=False)
    source = models.ForeignKey(
        'Source',
        db_column='source_id',
        verbose_name=_('source'),
        help_text=_('Source of item (parsing function and parent directory)'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    source_foreign_key = models.CharField(
        db_column='source_foreign_key',
        verbose_name=_('source foreign key'),
        help_text=_('Foreign key of file in source database'),
        max_length=64,
        blank=True)
    metadata = JSONField(
        db_column='metadata',
        default=empty_JSON,
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to item'),
        blank=True,
        null=True)
    captured_on = models.DateTimeField(
        db_column='captured_on',
        verbose_name=_('captured on'),
        help_text=_('Date on which item was produced'),
        blank=True,
        null=True)
    captured_on_year = models.IntegerField(
        db_column='captured_on_year',
        verbose_name=_('year'),
        help_text=_('Year in which the item was captured (YYYY)'),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1800),
            MaxValueValidator(3000)])
    captured_on_month = models.IntegerField(
        db_column='captured_on_month',
        verbose_name=_('month'),
        help_text=_('Month in which the item was captured (1-12)'),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(12)])
    captured_on_day = models.IntegerField(
        db_column='captured_on_day',
        verbose_name=_('day'),
        help_text=_('Day in which the item was captured'),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(32)])
    captured_on_hour = models.IntegerField(
        db_column='captured_on_hour',
        verbose_name=_('hour'),
        help_text=_('Hour of the day in which the item was captured (0 - 23)'),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(23)])
    captured_on_minute = models.IntegerField(
        db_column='captured_on_minute',
        verbose_name=_('minute'),
        help_text=_('Minute in which the item was captured (0-59)'),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(59)])
    captured_on_second = models.IntegerField(
        db_column='captured_on_second',
        verbose_name=_('second'),
        help_text=_('Second in which the item was captured (0-59)'),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(59)])
    licence = models.ForeignKey(
        'Licence',
        db_column='licence_id',
        verbose_name=_('licence'),
        help_text=_('Licence of item'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)

    tags = models.ManyToManyField(
        'Tag',
        verbose_name=_('tags'),
        help_text=_('Tags for item'),
        blank=True)
    ready_event_types = models.ManyToManyField(
        'EventType',
        verbose_name=_('ready event types'),
        help_text=_('Types of event for which item has been fully annotated'),
        blank=True)

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')

        ordering = ['created_on']

        permissions = (
            ("download_item", _("Can download item")),
            ("annotate_item", _("Can annotate item")),
        )

    def __str__(self):
        return str(self.id)  # pylint: disable=E1101

    def validate_user(self):
        if self.created_by is None:
            self.created_by = self.sampling_event_device.created_by  # pylint: disable=E1101

        if self.created_by is None:
            msg = _(
                'Item creator was not specified and is not determined '
                'by sampling event device.')
            raise ValidationError(msg)

        # TODO: Validate User

    @property
    def collection(self):
        return self.sampling_event_device.sampling_event.collection

    def clean(self):
        self.check_captured_on()
        try:
            self.validate_hash_and_filesize()
        except ValidationError as error:
            raise ValidationError({'hash': error})

        try:
            self.validate_user()
        except ValidationError as error:
            raise ValidationError({'created_by': error})

        try:
            self.item_type.validate_media_info(self.media_info)  # pylint: disable=E1101
        except ValidationError as error:
            raise ValidationError({'media_info': error})

        collection = (
            self.sampling_event_device  # pylint: disable=E1101
            .sampling_event.collection)

        try:
            collection.validate_and_get_sampling_event_type(
                self.sampling_event_device.sampling_event.sampling_event_type)  # pylint: disable=E1101
        except ValidationError as error:
            raise ValidationError({'sampling': error})

        try:
            collection_item_type = collection.validate_and_get_item_type(
                self.item_type)
        except ValidationError as error:
            raise ValidationError({'item_type': error})

        if collection_item_type is not None:
            try:
                collection_item_type.validate_metadata(self.metadata)
            except ValidationError as error:
                raise ValidationError({'metadata': error})

        try:
            self.validate_licence()
        except ValidationError as error:
            raise ValidationError({'licence': error})

        try:
            self.validate_mime_type()
        except ValidationError as error:
            raise ValidationError({'item_file': error})

        super(Item, self).clean()

    def validate_mime_type(self):
        if self.item_file.name is None:
            return

        file_mime_type, enc = mimetypes.guess_type(self.item_file.name)
        if self.item_type.media_type != file_mime_type:  # pylint: disable=E1101
            msg = _(
                'File MIME type does not coincide with declared item type '
                '(file: {file_type} != {item_type} :item_type)')
            params = dict(
                file_type=file_mime_type,
                item_type=self.item_type.media_type)  # pylint: disable=E1101
            raise ValidationError(msg % params)

    def validate_and_get_event_type(self, event_type):
        return self.item_type.validate_and_get_event_type(event_type)  # pylint: disable=E1101

    def validate_licence(self):
        if self.licence is not None:
            return

        if self.sampling_event_device.licence is None:  # pylint: disable=E1101
            msg = _(
                'Licence was not provided to item nor to sampling event')
            raise ValidationError({'licence': msg})

        self.licence = self.sampling_event_device.licence  # pylint: disable=E1101

        collection = self.sampling_event_device.sampling_event.collection  # pylint: disable=E1101
        collection.validate_and_get_licence(self.licence)

    def validate_hash_and_filesize(self):
        if self.item_file.name is None and self.hash is None:
            msg = _(
                'If no file is provided, a hash must be given')
            raise ValidationError(msg)

        if self.item_file.name is None:
            return

        self.item_file.open() # pylint: disable=E1101
        hash_string = hash_file(self.item_file)
        item_size = self.item_file.size  # pylint: disable=E1101
        print('item size', item_size)

        if self.hash is '':
            self.hash = hash_string
            self.filesize = item_size

        if self.hash != hash_string:
            msg = _('Hash of file and recorded hash do not coincide')
            raise ValidationError(msg)

    def add_ready_event_type(self, event_type):
        self.ready_event_types.add(event_type)  # pylint: disable=E1101
        self.save()

    def remove_ready_event_type(self, event_type):
        self.ready_event_types.remove(event_type)  # pylint: disable=E1101
        self.save()

    def add_tag(self, tag):
        self.tags.add(tag)  # pylint: disable=E1101
        self.save()

    def remove_tag(self, tag):
        self.tags.remove(tag)  # pylint: disable=E1101
        self.save()

    def delete(self, *args, **kwargs):
        self.item_file.delete()
        super().delete(*args, **kwargs)

    def check_captured_on(self):
        if self.captured_on is not None:
            return

        if (self.captured_on_year and self.captured_on_month and self.captured_on_day):

            if (self.captured_on_hour is not None and self.captured_on_minute is not None and self.captured_on_second is not None):

                self.captured_on = '{year}-{month}-{day} {hour}:{minute}:{second}'.format(
                    year=self.captured_on_year,
                    month=self.captured_on_month,
                    day=self.captured_on_day,
                    hour=self.captured_on_hour,
                    minute=self.captured_on_minute,
                    second=self.captured_on_second)

            else:
                self.captured_on = '{year}-{month}-{day}'.format(
                    year=self.captured_on_year,
                    month=self.captured_on_month,
                    day=self.captured_on_day)