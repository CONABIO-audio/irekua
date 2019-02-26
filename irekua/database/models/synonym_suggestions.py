from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class SynonymSuggestion(models.Model):
    source = models.ForeignKey(
        'Term',
        on_delete=models.CASCADE,
        db_column='source_id',
        verbose_name='')
    synonym = models.CharField(
        max_length=128,
        db_column='synonym',
        verbose_name=_('synonym'),
        help_text=_('Suggestion of synonym'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of synonym'),
        blank=True)
    metadata_type = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        db_column='metadata_type',
        verbose_name=_('metadata type'),
        help_text=_('Schema for synonym suggestion metadata'),
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
        help_text=_('Metadata associated to synonym'),
        null=True)
    suggested_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='suggested_by',
        verbose_name=_('suggested by'),
        help_text=_('User who made the synonym suggestion'),
        null=False,
        blank=False)
    suggested_on = models.DateTimeField(
        db_column='suggested_on',
        verbose_name=_('suggested on'),
        help_text=_('Date of synonym suggestion'),
        auto_now_add=True)

    class Meta:
        ordering = ['-suggested_on']
        verbose_name = _('Synonym Suggestion')
        verbose_name = _('Synonym Suggestions')

    def __str__(self):
        msg = _('Suggestion: {term} = {suggestion}').format(
            term=str(self.source),
            suggestion=self.synonym)
        return msg
