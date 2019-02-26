from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class TermSuggestion(models.Model):
    term_type = models.CharField(
        max_length=50,
        db_column='term_type',
        verbose_name=_('term type'),
        help_text=_('Type of term'),
        blank=False)
    value = models.CharField(
        max_length=50,
        db_column='value',
        verbose_name=_('value'),
        help_text=_('Value of term'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of term'),
        blank=True)
    metadata_type = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        db_column='metadata_type',
        verbose_name=_('metadata type'),
        help_text=_('Schema for term suggestion metadata'),
        limit_choices_to=(
            models.Q(field__exact='term_metadata') |
            models.Q(field__exact='global')),
        to_field='name',
        default='free',
        blank=False,
        null=False)
    metadata = JSONField(
        blank=True,
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to term'),
        null=True)
    suggested_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='suggested_by',
        verbose_name=_('suggested by'),
        help_text=_('User who made the term suggestion'),
        null=False,
        blank=False)
    suggested_on = models.DateTimeField(
        db_column='suggested_on',
        verbose_name=_('suggested on'),
        help_text=_('Date of term suggestion'),
        auto_now_add=True)

    class Meta:
        ordering = ['-suggested_on']
        verbose_name = _('Term Suggestion')
        verbose_name = _('Term Suggestions')

    def __str__(self):
        msg = _('Suggestion: {term_type}: {value}').format(
            term_type=self.term_type,
            value=self.value)
        return msg
