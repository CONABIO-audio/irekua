from django.db import models
from django.utils.translation import gettext_lazy as _

from database.models.schemas import Schema


class TermType(models.Model):
    name = models.CharField(
        max_length=128,
        primary_key=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name for term type'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of term type'),
        blank=False)
    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Term type icon'),
        upload_to='images/term_types/',
        blank=True,
        null=True)
    is_categorical = models.BooleanField(
        db_column='is_categorical',
        verbose_name=_('is categorical'),
        help_text=_('Flag indicating whether the term type represents a categorical variable'),
        blank=False,
        null=False)
    metadata_schema = models.ForeignKey(
        'Schema',
        related_name='term_metadata_type',
        on_delete=models.PROTECT,
        db_column='metadata_type',
        verbose_name=_('metadata type'),
        help_text=_('Metadata for terms of type'),
        limit_choices_to=(
            models.Q(field__exact=Schema.TERM_METADATA) |
            models.Q(field__exact=Schema.GLOBAL)),
        to_field='name',
        default=Schema.FREE_SCHEMA,
        blank=False,
        null=False)
    synonym_metadata_schema = models.ForeignKey(
        'Schema',
        related_name='term_synonym_metadata_type',
        on_delete=models.PROTECT,
        db_column='synonym_metadata_type',
        verbose_name=_('synonym metadata type'),
        help_text=_('Metadata for synonym of terms of type'),
        limit_choices_to=(
            models.Q(field__exact=Schema.SYNONYM_METADATA) |
            models.Q(field__exact=Schema.GLOBAL)),
        to_field='name',
        default=Schema.FREE_SCHEMA,
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Term Type')
        verbose_name_plural = _('Term Types')

    def __str__(self):
        return self.name

    class InvalidTermValue(Exception):
        pass

    def is_valid_non_categorical_value(self, value):
        return isinstance(value, (int, float))

    def is_valid_categorical_value(self, value):
        try:
            self.term_set.get(value=value)
            return True
        except self.term_set.model.DoesNotExist:
            return False

    def is_valid_value(self, value):
        if self.is_categorical:
            return self.is_valid_categorical_value(value)
        else:
            return self.is_valid_non_categorical_value(value)
