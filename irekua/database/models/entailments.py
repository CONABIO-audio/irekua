from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Entailment(models.Model):
    source = models.ForeignKey(
        'Term',
        related_name='entailment_source',
        db_column='source_id',
        verbose_name=_('source id'),
        help_text=_('Source of entailment'),
        on_delete=models.CASCADE,
        blank=False)
    target = models.ForeignKey(
        'Term',
        related_name='entailment_target',
        db_column='target_id',
        verbose_name=_('target id'),
        help_text=_('Target of entailment'),
        on_delete=models.CASCADE,
        blank=False)
    metadata_type = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        db_column='metadata_type',
        verbose_name=_('metadata type'),
        help_text=_('JSON schema for entailment metadata'),
        limit_choices_to=(
            models.Q(field__exact='entailment_metadata') |
            models.Q(field__exact='global')),
        to_field='name',
        default='free',
        blank=False,
        null=False)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to entailment'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Entailment')
        verbose_name_plural = _('Entailments')

    def __str__(self):
        msg = '{source} => {target}'.format(
            source=self.source,
            target=self.target)
        return msg
