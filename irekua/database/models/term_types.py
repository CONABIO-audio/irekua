from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from database.models.schemas import Schema


class TermType(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
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
        db_column='metadata_schema_id',
        verbose_name=_('metadata schema'),
        help_text=_('JSON schema for metadata of terms of type'),
        limit_choices_to=(
            models.Q(field__exact=Schema.TERM_METADATA) |
            models.Q(field__exact=Schema.GLOBAL)),
        to_field='name',
        default=Schema.FREE_SCHEMA,
        blank=False,
        null=False)
    synonym_metadata_schema = models.ForeignKey(
        'Schema',
        related_name='term_synonym_metadata_schema',
        on_delete=models.PROTECT,
        db_column='synonym_metadata_schema_id',
        verbose_name=_('synonym metadata schema'),
        help_text=_('JSON schema for metadata of synonyms of terms of type'),
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

    def validate_non_categorical_value(self, value):
        if not isinstance(value, (int, float)):
            msg = _('Value %(value)s is invalid for non-categorical term of type %(type)')
            params = dict(value=value, type=str(self))
            raise ValidationError(msg, params=params)

    def validate_categorical_value(self, value):
        try:
            self.term_set.get(value=value)
        except self.term_set.model.DoesNotExist:
            msg = _('Value %(value) is invalid for categorical term of type %(type)')
            params = dict(value=value, type=str(self))
            raise ValidationError(msg, params=params)

    def validate_value(self, value):
        if self.is_categorical:
            return self.validate_categorical_value(value)

        return self.validate_non_categorical_value(value)

    def validate_metadata(self, metadata):
        try:
            self.metadata_schema.validate_instance(metadata)
        except ValidationError as error:
            msg = _('Invalid metadata for term of type %(type)s. Error: %(error)s')
            params = dict(type=str(self), error=str(error))
            raise ValidationError(msg, params=params)

    def validate_synonym_metadata(self, metadata):
        try:
            self.synonym_metadata_schema.validate_instance(metadata)
        except ValidationError as error:
            msg = _('Invalid metadata for synonym of terms of type %(type)s. Error: %(error)s')
            params = dict(type=str(self), error=str(error))
            raise ValidationError(msg, params=params)
