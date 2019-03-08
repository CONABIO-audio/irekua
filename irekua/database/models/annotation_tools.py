from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from database.models.schemas import Schema


class AnnotationTool(models.Model):
    name = models.CharField(
        max_length=64,
        primary_key=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of annotation tool'),
        blank=False)
    version = models.CharField(
        max_length=16,
        db_column='version',
        verbose_name=_('version'),
        help_text=_('Version of annotation tool'),
        blank=True)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of annotation tool'),
        blank=False)
    logo = models.ImageField(
        db_column='logo',
        verbose_name=_('logo'),
        help_text=_('Annotation tool logo'),
        upload_to='images/annotation_tools/',
        blank=True,
        null=True)
    url = models.URLField(
        db_column='url',
        verbose_name=_('url'),
        help_text=_('Resource location'),
        blank=True,
        null=True)
    configuration_schema = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        db_column='configuration_schema_id',
        verbose_name=_('configuration schema'),
        help_text=_('JSON schema for configuration of annotation tool'),
        limit_choices_to=(
            models.Q(field__exact=Schema.ANNOTATION_CONFIGURATION) |
            models.Q(field__exact=Schema.GLOBAL)),
        blank=False,
        null=False,
        to_field='name',
        default=Schema.FREE_SCHEMA)

    class Meta:
        verbose_name = _('Annotation Tool')
        verbose_name_plural = _('Annotation Tools')

    def __str__(self):
        msg = self.name
        if self.version:
            msg += ' - ' + self.version
        return msg

    def validate_configuration(self, configuration):
        try:
            self.configuration_schema.validate_instance(configuration)
        except ValidationError as error:
            msg = _('Invalid annotation tool configuration. Error: %(error)s')
            params = dict(error=str(error))
            raise ValidationError(msg, params=params)
