from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from database.models.schemas import Schema


class Entailment(models.Model):
    source = models.ForeignKey(
        'Term',
        related_name='entailment_source',
        db_column='source_id',
        verbose_name=_('source'),
        help_text=_('Source of entailment'),
        on_delete=models.CASCADE,
        blank=False)
    target = models.ForeignKey(
        'Term',
        related_name='entailment_target',
        db_column='target_id',
        verbose_name=_('target'),
        help_text=_('Target of entailment'),
        on_delete=models.CASCADE,
        blank=False)
    metadata_schema = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        db_column='metadata_schema_id',
        verbose_name=_('metadata schema'),
        help_text=_('JSON schema for entailment metadata'),
        limit_choices_to=(
            models.Q(field__exact=Schema.ENTAILMENT_METADATA) |
            models.Q(field__exact=Schema.GLOBAL)),
        to_field='name',
        default=Schema.FREE_SCHEMA,
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
        msg = '%(source)s => %(target)s'
        params = dict(
            source=str(self.source),
            target=str(self.target))
        return msg % params

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
    def clean(self):
        try:
            self.metadata_schema.validate_instance(self.metadata)
        except ValidationError as error:
            msg = _('Invalid entailment metadata. Error %(error)s')
            params = dict(error=str(error))
            raise ValidationError(msg, params=params)

        super(Entailment, self).clean()
