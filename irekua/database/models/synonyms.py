from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Synonym(models.Model):
    source = models.ForeignKey(
        'Term',
        related_name='synonym_source',
        on_delete=models.CASCADE,
        db_column='source_id',
        verbose_name=_('source id'),
        help_text=_('Reference to the source of synonym'),
        blank=False)
    target = models.ForeignKey(
        'Term',
        related_name='synonym_target',
        on_delete=models.CASCADE,
        db_column='target_id',
        verbose_name=_('target id'),
        help_text=_('Reference to the target of the synonym'),
        blank=False)
    metadata_type = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        db_column='metadata_type',
        verbose_name=_('metadata type'),
        help_text=_('Schema for synonym metadata'),
        limit_choices_to=(
            models.Q(field__exact='synonym_metadata') |
            models.Q(field__exact='global')),
        to_field='name',
        default='free',
        blank=False,
        null=False)
    metadata = JSONField(
        blank=True,
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to the synonym'),
        null=True)

    class Meta:
        verbose_name = _('Synonym')
        verbose_name_plural = _('Synonyms')

    def __str__(self):
        msg = '{source} = {target}'.format(
            source=str(self.source),
            target=str(self.target))
        return msg
