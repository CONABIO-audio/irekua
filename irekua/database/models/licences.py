from django.contrib.postgres.fields import JSONField
from django.db import models
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
    document = models.CharField(
        max_length=128,
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
        blank=False)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        default=empty_JSON,
        help_text=_('Metadata associated with licence'),
        blank=True,
        null=True)

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
        try:
            self.licence_type.validate_metadata(self.metadata)
        except ValidationError as error:
            raise ValidationError({'metadata': error})
        super(Licence, self).clean()

    def is_invalid(self):
        now = timezone.now()
        timedelta = now - self.created_on
        print(timedelta)
