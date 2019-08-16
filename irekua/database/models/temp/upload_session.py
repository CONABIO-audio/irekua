from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from database.utils import empty_JSON
from database.models.base import IrekuaModelBaseUser


class UploadSession(IrekuaModelBaseUser):
    sampling_event_device = models.ForeignKey(
        'SamplingEventDevice',
        db_column='sampling_event_device_id',
        verbose_name=_('sampling event device'),
        help_text=_('Sampling event device used to create item'),
        on_delete=models.PROTECT,
        blank=False,
        null=False)
    configuration = JSONField(
        db_column='configuration',
        verbose_name=_('configuration'),
        help_text=_('Configuration for this upload session'),
        default=empty_JSON,
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Upload Session')
        verbose_name_plural = _('Upload Sessions')
        ordering = ['-created_on']

    def __str__(self):
        return str(self.id)

    @property
    def upload_events(self):
        queryset = UploadEvent.objects.filter(
            upload_session=self)
        return queryset

    def validate_user(self):
        if self.created_by is None:
            msg = _(
                'Session creator was not specified')
            raise ValidationError(msg)

    def clean(self):
        try:
            self.validate_user()
        except ValidationError as error:
            raise ValidationError({'created_by': error})

        super(UploadSession, self).clean()