from django.db import models
from django.utils.translation import gettext_lazy as _


class LicenceType(models.Model):
    name = models.CharField(
        max_length=128,
        primary_key=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Licence type name'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of licence'),
        blank=False)
    metadata_schema = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        db_column='metadata_schema',
        verbose_name=_('metadata schema'),
        help_text=_('Schema for licence metadata structure'),
        limit_choices_to=(
            models.Q(field__exact='licence_metadata') |
            models.Q(field__exact='global')),
        to_field='name',
        default='free',
        blank=False,
        null=False)
    document_template = models.CharField(
        max_length=128,
        unique=True,
        db_column='document_template',
        verbose_name=_('document template'),
        help_text=_('Template for licence document'),
        blank=True)
    can_view = models.BooleanField(
        db_column='can_view',
        verbose_name=_('can view'),
        help_text=_('Any user can view item info'),
        blank=False,
        null=False)
    can_download = models.BooleanField(
        db_column='can_download',
        verbose_name=_('can download'),
        help_text=_('Any user can download item'),
        blank=False,
        null=False)
    can_view_annotations = models.BooleanField(
        db_column='can_view_annotations',
        verbose_name=_('can view annotations'),
        help_text=_('Any user can view item annotations'),
        blank=False,
        null=False)
    can_annotate = models.BooleanField(
        db_column='can_annotate',
        verbose_name=_('can annotate'),
        help_text=_('Any user can annotate item'),
        blank=False,
        null=False)
    can_vote_annotations = models.BooleanField(
        db_column='can_vote_annotations',
        verbose_name=_('can vote annotations'),
        help_text=_('Any user can vote on item annotations'),
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Licence Type')
        verbose_name_plural = _('Licence Types')

    def __str__(self):
        return self.name
