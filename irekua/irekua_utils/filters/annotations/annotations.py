from django import forms
from django.db import models
from django.utils.translation import gettext as _
from django_filters import FilterSet,DateFilter

from database.models import Annotation


class Filter(FilterSet):
    class Meta:
        model = Annotation
        fields = {
            'annotation_type': ['exact'],
            'event_type': ['exact'],
            'created_by__username': ['icontains'],
            'created_by__first_name': ['icontains'],
            'created_by__last_name': ['icontains'],
            'certainty' : ['gt', 'lt'],
            'created_on': ['gt', 'lt'],
            }

        filter_overrides = {
            models.DateTimeField: {
                'filter_class': DateFilter,
                'extra': lambda f: {
                    'widget': forms.DateInput(attrs={'class': 'datepicker'})
                }
            }
        }


search_fields = (
    'annotation_type',
    'event_type',
    'created_by__username',
    'created_on'
)

ordering_fields = (
    ('created_on', _('added on')),
    ('annotation_type', _('annotation type')),
    ('event_type', _('event type')),


)
