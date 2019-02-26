from django.db import models
from django.utils.translation import gettext_lazy as _


class AnnotationType(models.Model):
    name = models.CharField(
        max_length=32,
        primary_key=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name for type of annotation'))
    description = models.TextField(
        null=False,
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of annotation type'))
    schema = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        db_column='schema_id',
        verbose_name=_('schema id'),
        limit_choices_to=(
            models.Q(field__exact='annotation_annotation') |
            models.Q(field__exact='global')),
        help_text=_('JSON schema for annotation type'))

    class Meta:
        verbose_name = _('Annotation Type')
        verbose_name_plural = _('Annotation Types')

    def __str__(self):
        return self.name
