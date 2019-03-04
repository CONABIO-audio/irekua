from django.contrib.postgres.fields import JSONField, HStoreField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from database.utils import (
    validate_json_instance,
    empty_json,
)


class Annotation(models.Model):
    QUALITY_OPTIONS = [
        ('L', _('low')),
        ('M', _('medium')),
        ('H', _('high')),
    ]

    annotation_tool = models.ForeignKey(
        'AnnotationTool',
        on_delete=models.PROTECT,
        db_column='annotation_tool',
        verbose_name=_('annotation tool'),
        help_text=_('Annotation tool used'),
        blank=False)
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
    label = HStoreField(
        db_column='label',
        verbose_name=_('label'),
        help_text=_('Labels associated to annotation'),
        default=empty_json,
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
        default=empty_json,
        help_text=_('Information of annotation location within item'),
        blank=False,
        null=False)
    annotation_configuration = JSONField(
        db_column='annotation_configuration',
        verbose_name=_('annotation configuration'),
        default=empty_json,
        help_text=_('Configuration of annotation tool'),
        blank=False,
        null=False)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        default=empty_json,
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
        editable=False,
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
        # TODO
        validate_json_instance(
            self.metadata,
            self.metadata_type.schema)

        try:
            self.annotation_type.validate_annotation(self.annotation)
        except ValidationError as error:
            raise ValidationError({'annotation': error})

        try:
            self.annotation_tool.validate_configuration(self.annotation_configuration)
        except ValidationError as error:
            raise ValidationError({'annotation_configuration': error})

        
        self.item.validate_annotation(self)
        self.validate_label(self.label)
        super(Annotation, self).clean(*args, **kwargs)

    def validate_label(self, label):
        for key, value in label.items():
            try:
                term_type = self.event_type.get_term_type_or_none(key)
            except self.event_type.InvalidTermType:
                msg = _('Label contains a term type ({type}) that is not valid for the event type or does not exist')
                msg = msg.format(type=key)
                raise ValidationError({'label': msg})

            if not term_type.is_valid_value(value):
                msg = _('{value} is not a valid value for term type {type}')
                msg = msg.format(value=value, type=str(term_type))
                raise ValidationError({'label': msg})
