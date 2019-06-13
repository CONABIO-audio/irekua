from django.contrib.postgres.fields import HStoreField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from database.utils import empty_JSON
from database.models.base import IrekuaModelBaseUser


class AnnotationVote(IrekuaModelBaseUser):
    annotation = models.ForeignKey(
        'Annotation',
        on_delete=models.CASCADE,
        db_column='annotation_id',
        verbose_name=_('annotation'),
        help_text=_('Reference to annotation being voted'),
        blank=False,
        null=False)
    label = HStoreField(
        db_column='label',
        verbose_name=_('label'),
        default=empty_JSON,
        help_text=_('Labels associated to annotation vote'),
        blank=False,
        null=False)

    class Meta:
        ordering = ['-modified_on']
        verbose_name = _('Annotation Vote')
        verbose_name_plural = _('Annotation Votes')

    def __str__(self):
        msg = _('Vote %(id)s on annotation %(annotation)s')
        params = dict(id=self.id, annotation=self.annotation.id)
        return msg % params

    def clean(self):
        try:
            self.annotation.validate_label(self.label)
        except ValidationError as error:
            msg = _('Invalid label for event type %(type)s. Error: %(error)s')
            params = dict(
                type=str(self.annotation.event_type),
                error=str(error))
            raise ValidationError({'label': msg % params})
        super(AnnotationVote, self).clean()
