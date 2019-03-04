from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

from database.utils import (
    validate_json_instance,
    validate_are_same_term_type,
    empty_json
)


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
    metadata = JSONField(
        blank=True,
        db_column='metadata',
        default=empty_json,
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

    def clean(self, *args, **kwargs):
        validate_are_same_term_type(
            self.source,
            self.target)
        validate_json_instance(
            self.metadata,
            self.source.term_type.synonym_metadata_schema.schema)
        super(Synonym, self).clean(*args, **kwargs)
