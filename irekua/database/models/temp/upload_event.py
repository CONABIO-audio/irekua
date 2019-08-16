from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from database.models.base import IrekuaModelBaseUser



class UploadEvent(IrekuaModelBaseUser):
    upload_session = models.ForeignKey(
        'UploadSession',
        db_column='upload_session_id',
        verbose_name=_('upload session'),
        help_text=_('Upload session'),
        on_delete=models.PROTECT,
        blank=False,
        null=False)
    error = models.CharField(
        db_column='error',
        verbose_name=_('error'),
        help_text=_('Type of error (if apply)'),
        max_length=64,
        blank=True)
    item = models.ForeignKey(
        'Item',
        db_column='item_id',
        verbose_name=_('item'),
        help_text=_('Created item (if apply)'),
        on_delete=models.PROTECT,
        blank=True)

    class Meta:
        verbose_name = _('Upload Session')
        verbose_name_plural = _('Upload Sessions')

        ordering = ['-created_on']

    def __str__(self):
        return str(self.id)

    def validate_user(self):
        if self.created_by is None:
            self.created_by = self.upload_session.created_by

        if self.created_by is None:
            msg = _(
                'UploadEvent creator was not specified')
            raise ValidationError(msg)

    def clean(self):
        try:
            self.validate_user()
        except ValidationError as error:
            raise ValidationError({'created_by': error})

        super(UploadEvent, self).clean()