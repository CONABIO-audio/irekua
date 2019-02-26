from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class AnnotationVote(models.Model):
    annotation = models.ForeignKey(
        'Annotation',
        on_delete=models.CASCADE,
        db_column='annotation_id',
        verbose_name=_('annotation id'),
        help_text=_('Reference to annotation being voted'),
        blank=False,
        null=False)
    label = JSONField(
        db_column='label',
        verbose_name=_('label'),
        help_text=_('Labels associated to annotation vote'),
        blank=False,
        null=False)
    created_by = models.ForeignKey(
        User,
        db_column='created_by',
        verbose_name=_('created by'),
        help_text=_('Creator of annotation vote'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    created_on = models.DateTimeField(
        db_column='created_on',
        verbose_name=_('created on'),
        help_text=_('Date of creation of annotation'),
        editable=False,
        auto_now_add=True)
    modified_on = models.DateTimeField(
        db_column='modified_on',
        verbose_name=_('modified on'),
        help_text=_('Date of last modification'),
        editable=False,
        auto_now=True)

    class Meta:
        ordering = ['-modified_on']
        verbose_name = _('Annotation Vote')
        verbose_name_plural = _('Annotation Votes')

    def __str__(self):
        msg = _('Vote {id} on annotation {annotation}').format(
            id=self.id,
            annotation=self.annotation.id)
        return msg
