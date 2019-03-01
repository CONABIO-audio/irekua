from django.db import models
from django.utils.translation import gettext_lazy as _


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
    metadata_type = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        db_column='metadata_type',
        verbose_name=_('metadata type'),
        help_text=_('Metadata for terms of type'),
        limit_choices_to=(
            models.Q(field__exact='term_metadata') |
            models.Q(field__exact='global')),
        to_field='name',
        default='free',
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Term Type')
        verbose_name_plural = _('Term Types')

    def __str__(self):
        return self.name
