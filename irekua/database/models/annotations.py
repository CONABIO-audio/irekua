from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from database.utils import (
    validate_json_instance,
    validate_is_of_collection,
)


class Annotation(models.Model):
    QUALITY_OPTIONS = [
        ('L', _('low')),
        ('M', _('medium')),
        ('H', _('high')),
    ]

    item = models.ForeignKey(
        'Item',
        db_column='item_id',
        verbose_name=_('item id'),
        help_text=_('Annotated item'),
        limit_choices_to={'is_uploaded': True},
        on_delete=models.PROTECT,
        blank=False)
    event_type = models.ForeignKey(
        'EventType',
        on_delete=models.PROTECT,
        db_column='event_type',
        verbose_name=_('event type'),
        help_text=_('Type of event being annotated'),
        blank=False)
    label_type = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        related_name='annotation_label_type',
        db_column='label_type',
        verbose_name=_('label type'),
        help_text=_('Schema for label structure'),
        limit_choices_to=(
            models.Q(field__exact='annotation_label') |
            models.Q(field__exact='global')),
        to_field='name',
        default='free',
        blank=False,
        null=False)
    label = JSONField(
        db_column='label',
        verbose_name=_('label'),
        help_text=_('Labels associated to annotation'),
        blank=False,
        null=False)
    annotation_type = models.ForeignKey(
        'AnnotationType',
        on_delete=models.PROTECT,
        db_column='annotation_type',
        verbose_name=_('annotation type'),
        help_text=_('Type of annotation'),
        blank=False)
    annotation = JSONField(
        db_column='annotation',
        verbose_name=_('annotation'),
        help_text=_('Information of annotation location within item'),
        blank=False,
        null=False)
    metadata_type = models.ForeignKey(
        'Schema',
        related_name='annotation_metadata_type',
        on_delete=models.PROTECT,
        db_column='metadata_type',
        verbose_name=_('metadata type'),
        help_text=_('JSON schema for metadata'),
        limit_choices_to=(
            models.Q(field__exact='annotation_metadata') |
            models.Q(field__exact='global')),
        blank=True,
        null=True,
        to_field='name',
        default='free')
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to annotation'),
        blank=False)
    certainty = models.FloatField(
        db_column='certainty',
        verbose_name=_('certainty'),
        help_text=_('Level of certainty of location or labelling of annotation'),
        blank=True,
        null=True)
    quality = models.CharField(
        db_column='quality',
        verbose_name=_('quality'),
        help_text=_('Quality of item content inside annotation'),
        blank=True,
        max_length=10,
        choices=QUALITY_OPTIONS)
    commentaries = models.TextField(
        db_column='commentaries',
        verbose_name=_('commentaries'),
        help_text=_('Commentaries of annotator'),
        blank=True)
    created_on = models.DateTimeField(
        db_column='created_on',
        verbose_name=_('created on'),
        help_text=_('Date of creation of annotation'),
        editable=False,
        auto_now_add=True)
    modified_on = models.DateTimeField(
        db_column='modified_on',
        verbose_name=_('modified on'),
        help_text=_('Date of last modification'),
        editable=False,
        auto_now=True)
    created_by = models.ForeignKey(
        User,
        related_name='annotation_created_by',
        db_column='created_by',
        verbose_name=_('created by'),
        help_text=_('Creator of annotation'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    last_modified_by = models.ForeignKey(
        User,
        related_name='annotation_last_modified_by',
        db_column='last_modified_by',
        verbose_name=_('last modified by'),
        help_text=_('User that modified the annotation last'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Annotation')
        verbose_name_plural = _('Annotations')

    def __str__(self):
        msg = _('Annotation {annotation_id} of item {item_id}').format(
            annotation_id=self.id,
            item_id=self.item.id)
        return msg

    def clean(self, *args, **kwargs):
        validate_json_instance(self.label, self.label_type.schema)
        validate_json_instance(self.annotation, self.annotation_type.schema)
        validate_json_instance(self.metadata, self.metadata_type.schema)

        collection = self.item.collection
        if collection is not None:
            validate_is_of_collection(
                collection,
                self.annotation_type.schema)
            validate_is_of_collection(
                collection,
                self.metadata_type.schema)

        super(Annotation, self).clean(*args, **kwargs)
