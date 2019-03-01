from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

from database.utils import validate_json_instance


class Term(models.Model):
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
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to term'),
        blank=True,
        null=True)

    class Meta:
        ordering = ['term_type', 'value']
        verbose_name = _('Term')
        verbose_name_plural = _('Terms')

    def __str__(self):
        msg = '{term_type}: {value}'.format(
            term_type=self.term_type,
            value=self.value)
        return msg

    def clean(self, *args, **kwargs):
        metadata_schema = self.term_type.metadata_type.schema
        validate_json_instance(self.metadata, metadata_schema)
        super(Term, self).clean(*args, **kwargs)
