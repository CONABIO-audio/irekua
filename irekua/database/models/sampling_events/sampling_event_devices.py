from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from database.utils import empty_JSON


class SamplingEventDevice(models.Model):
    sampling_event = models.ForeignKey(
        'SamplingEvent',
        on_delete=models.PROTECT,
        db_column='sampling_event_id',
        verbose_name=_('sampling event'),
        help_text=_('Sampling event in which this device was deployed'),
        blank=False,
        null=False)

    collection_device = models.ForeignKey(
        'CollectionDevice',
        db_column='collection_device_id',
        verbose_name=_('collection device'),
        help_text=_('Reference to collection device used on sampling event'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    commentaries = models.TextField(
        db_column='commentaries',
        verbose_name=_('commentaries'),
        help_text=_('Sampling event commentaries'),
        blank=True)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to sampling event device'),
        default=empty_JSON,
        blank=True,
        null=True)
    configuration = JSONField(
        db_column='configuration',
        verbose_name=_('configuration'),
        default=empty_JSON,
        help_text=_('Configuration on device through the sampling event'),
        blank=True,
        null=True)
    licence = models.ForeignKey(
        'Licence',
        on_delete=models.PROTECT,
        db_column='licence_id',
        verbose_name=_('licence'),
        help_text=_('Licence for all items in sampling event'),
        blank=True,
        null=True)

    created_by = models.ForeignKey(
        'User',
        related_name='sampling_event_device_created_by',
        on_delete=models.PROTECT,
        db_column='created_by',
        verbose_name=_('create by'),
        help_text=_('Creator of sampling event device'),
        blank=True,
        null=True)
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
    modified_by = models.ForeignKey(
        'User',
        related_name='sampling_event_device_modified_by',
        on_delete=models.PROTECT,
        db_column='modified_by',
        verbose_name=_('modified by'),
        help_text=_('Last modifier'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Sampling Event Device')
        verbose_name_plural = _('Sampling Event Devices')

        ordering = ['-created_on']

    def __str__(self):
        msg = _('Collection device {device} in Sampling Event {event}')
        msg = msg.format(
            device=str(self.collection_device.id),
            event=str(self.sampling_event.id))
        return msg

    def validate_licence(self):
        if self.licence is not None:
            self.licence = self.sampling_event.licence

        if self.licence is not None:
            collection = self.sampling_event.collection
            collection.validate_and_get_licence(self.licence)

    def validate_user(self):
        if self.created_by is None:
            self.created_by = self.sampling_event.created_by

        if self.created_by is None:
            return

        # TODO: Validate user

    def clean(self):
        try:
            self.validate_licence()
        except ValidationError as error:
            raise ValidationError({'licence': error})

        try:
            sampling_event_type = (
                self.sampling_event.sampling_event_type)
            device_type = (
                self.collection_device.physical_device.device.device_type)

            sampling_event_device_type = (
                sampling_event_type.validate_and_get_device_type(
                    device_type))
        except ValidationError as error:
            raise ValidationError({'physical_device': error})

        if sampling_event_device_type is not None:
            try:
                sampling_event_device_type.validate_metadata(self.metadata)
            except ValidationError as error:
                raise ValidationError({'metadata': error})

        try:
            physical_device = self.collection_device.physical_device
            physical_device.validate_configuration(self.configuration)
        except ValidationError as error:
            raise ValidationError({'configuration': error})

        if self.licence is not None:
            collection = self.sampling_event.collection
            try:
                collection.validate_and_get_licence(self.licence)
            except ValidationError as error:
                raise ValidationError({'licence': error})

        super().clean()