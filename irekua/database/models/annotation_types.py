from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from database.models.schemas import Schema


class AnnotationType(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
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
        verbose_name=_('schema'),
        limit_choices_to=(
            models.Q(field__exact=Schema.ANNOTATION) |
            models.Q(field__exact=Schema.GLOBAL)),
        help_text=_('JSON schema for annotation type'))
    icon = models.ImageField(
        db_column='icon',
        upload_to='images/annotation_types/',
        verbose_name=_('icon'),
        help_text=_('Annotation type icon'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Annotation Type')
        verbose_name_plural = _('Annotation Types')

    def __str__(self):
        return self.name

    def validate_annotation(self, annotation):
        try:
            self.schema.validate_instance(annotation)
        except ValidationError as error:
            msg = _('Invalid annotation for annotation type %(type)s. Error: %(error)s')
            params = dict(type=str(self), error=str(error))
            raise ValidationError(msg, params=params)
