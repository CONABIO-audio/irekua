from django.contrib.postgres.fields import JSONField
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from database.utils import (
    empty_JSON,
)


class Licence(models.Model):
    licence_type = models.ForeignKey(
        'LicenceType',
        on_delete=models.PROTECT,
        db_column='licence_type_id',
        verbose_name=_('licence type'),
        help_text=_('Type of licence used'),
        blank=False,
        null=False)
    document = models.FileField(
        upload_to='documents/licences/',
        db_column='document',
        verbose_name=_('document'),
        help_text=_('Legal document of licence agreement'),
        blank=True)

    created_on = models.DateTimeField(
        editable=False,
        auto_now_add=True,
        db_column='created_on',
        verbose_name=_('created on'),
        help_text=_('Date of licence creation'),
        blank=True)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        default=empty_JSON,
        help_text=_('Metadata associated with licence'),
        blank=True,
        null=True)
    signed_by = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        db_column='signed_by',
        verbose_name=_('signed by'),
        help_text=_('User who signed the licence'),
        blank=True,
        null=True)
    collection = models.ForeignKey(
        'Collection',
        on_delete=models.CASCADE,
        db_column='collection_id',
        verbose_name=_('collection'),
        help_text=_('Collection to which this licence belongs'),
        blank=False,
        null=False)

    is_active = models.BooleanField(
        editable=False,
        db_column='is_active',
        verbose_name=_('is active'),
        help_text=_('Licence is still active'),
        default=False,
        blank=True,
        null=False)

    class Meta:
        verbose_name = _('Licence')
        verbose_name_plural = _('Licences')

        ordering = ['-created_on']

    def __str__(self):
        msg = _('Licence of type {type} created on {date}').format(
            type=str(self.licence_type),
            date=self.created_on)
        return msg

    def clean(self):
        self.update_is_active()
        try:
            self.licence_type.validate_metadata(self.metadata)
        except ValidationError as error:
            raise ValidationError({'metadata': error})
        super(Licence, self).clean()

    def update_is_active(self):
        # When licence is beign created the attribute created_on is null
        if self.created_on is None:
            self.is_active = True
            return

        duration_in_years = self.licence_type.years_valid_for
        current_time_offset = timezone.now() - self.created_on
        year_offset = current_time_offset.days / 365
        self.is_active = year_offset <= duration_in_years
