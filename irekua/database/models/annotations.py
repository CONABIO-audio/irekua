from django.contrib.postgres.fields import HStoreField, JSONField
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Annotation(models.Model):
    QUALITY_OPTIONS = [
        ('L', 'baja'),
        ('M', 'media'),
        ('H', 'alta')
    ]

    item = models.ForeignKey(
        'Item',
        db_column='item_id',
        verbose_name=_('item id'),
        help_text=_('Annotated item'),
        on_delete=models.PROTECT,
        blank=False)
    annotation_type = models.CharField(
        max_length=30,
        db_column='annotation_type',
        verbose_name=_('annotation type'),
        help_text=_('Type of annotation'),
        blank=False)
    event_type = models.CharField(
        max_length=30,
        db_column='event_type',
        verbose_name=_('event type'),
        help_text=_('Type of event being annotated'),
        blank=False)
    label = HStoreField(
        db_column='label',
        verbose_name=_('label'),
        help_text=_('Labels associated to annotation'),
        blank=False)
    annotation = JSONField(
        db_column='annotation',
        verbose_name=_('annotation'),
        help_text=_('Information of annotation location within item'),
        blank=False)
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
    model = models.ForeignKey(
        'Model',
        on_delete=models.PROTECT,
        db_column='model_id',
        verbose_name=_('model id'),
        help_text=_('Creator of annotation (AI model)'),
        blank=False)
    created_by = models.ForeignKey(
        User,
        db_column='created_by',
        verbose_name=_('created by'),
        help_text=_('Creator of annotation (User)'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)
