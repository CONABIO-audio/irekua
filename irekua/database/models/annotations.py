from django.contrib.postgres.fields import JSONField, HStoreField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from database.utils import (
    empty_JSON,
)


class Annotation(models.Model):
    LOW_QUALITY = 'L'
    MEDIUM_QUALITY = 'M'
    HIGH_QUALITY = 'H'
    QUALITY_OPTIONS = [
        (LOW_QUALITY, _('low')),
        (MEDIUM_QUALITY, _('medium')),
        (HIGH_QUALITY, _('high')),
    ]

    annotation_tool = models.ForeignKey(
        'AnnotationTool',
        on_delete=models.PROTECT,
        db_column='annotation_tool_id',
        verbose_name=_('annotation tool'),
        help_text=_('Annotation tool used'),
        blank=False)
    item = models.ForeignKey(
        'Item',
        db_column='item_id',
        verbose_name=_('item'),
        help_text=_('Annotated item'),
        on_delete=models.PROTECT,
        blank=False)
    event_type = models.ForeignKey(
        'EventType',
        on_delete=models.PROTECT,
        db_column='event_type_id',
        verbose_name=_('event type'),
        help_text=_('Type of event being annotated'),
        blank=False)
    label = HStoreField(
        db_column='label',
        verbose_name=_('label'),
        help_text=_('Labels associated to annotation'),
        default=empty_JSON,
        blank=False,
        null=False)
    annotation_type = models.ForeignKey(
        'AnnotationType',
        on_delete=models.PROTECT,
        db_column='annotation_type_id',
        verbose_name=_('annotation type'),
        help_text=_('Type of annotation'),
        blank=False)
    annotation = JSONField(
        db_column='annotation',
        verbose_name=_('annotation'),
        default=empty_JSON,
        help_text=_('Information of annotation location within item'),
        blank=False,
        null=False)
    annotation_configuration = JSONField(
        db_column='annotation_configuration',
        verbose_name=_('annotation configuration'),
        default=empty_JSON,
        help_text=_('Configuration of annotation tool'),
        blank=False,
        null=False)
    certainty = models.FloatField(
        db_column='certainty',
        verbose_name=_('certainty'),
        help_text=_(
            'Level of certainty of location or labelling '
            'of annotation'),
        blank=True,
        null=True)
    quality = models.CharField(
        db_column='quality',
        verbose_name=_('quality'),
        help_text=_('Quality of item content inside annotation'),
        blank=True,
        max_length=16,
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
        'User',
        related_name='annotation_created_by',
        db_column='created_by',
        verbose_name=_('created by'),
        help_text=_('Creator of annotation'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    modified_by = models.ForeignKey(
        'User',
        editable=False,
        related_name='annotation_modified_by',
        db_column='modified_by',
        verbose_name=_('modified by'),
        help_text=_('User that modified the annotation last'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Annotation')
        verbose_name_plural = _('Annotations')

        ordering = ['-modified_on']

        permissions = (
            ("vote", _("Can vote annotation")),
        )

    def __str__(self):
        msg = _('Annotation %(annotation_id)s of item %(item_id)s')
        params = dict(annotation_id=self.id, item_id=self.item)
        return msg % params

    def clean(self):
        try:
            self.item.validate_and_get_event_type(self.event_type)
        except ValidationError as error:
            raise ValidationError({'event_type': error})

        collection = self.item.sampling_event.collection
        try:
            collection.validate_and_get_event_type(self.event_type)
        except ValidationError as error:
            raise ValidationError({'event_type': error})

        try:
            collection.validate_and_get_annotation_type(self.annotation_type)
        except ValidationError as error:
            raise ValidationError({'annotation_type': error})

        try:
            self.annotation_type.validate_annotation(self.annotation)
        except ValidationError as error:
            raise ValidationError({'annotation': error})

        try:
            self.annotation_tool.validate_configuration(
                self.annotation_configuration)
        except ValidationError as error:
            raise ValidationError({'annotation_configuration': error})

        try:
            self.validate_label(self.label)
        except ValidationError as error:
            raise ValidationError({'label': error})

        super(Annotation, self).clean()

    def validate_label(self, label):
        for key, value in label.items():
            try:
                term_type = self.event_type.validate_and_get_term_type(key)
            except ValidationError:
                msg = _(
                    'Label contains a term (of type %(type)s) that is not '
                    'valid for the event type or does not exist')
                params = dict(type=key)
                raise ValidationError(msg, params=params)

            try:
                term_type.validate_value(value)
            except ValidationError as error:
                msg = _('Invalid label. Error: %(error)s')
                params = dict(error=str(error))
                raise ValidationError(msg, params=params)
