from django import forms
from django.db import models
from django.utils.translation import gettext as _
from django_filters import FilterSet,DateFilter

from database.models import SamplingEvent


class Filter(FilterSet):
    class Meta:
        model = SamplingEvent
        fields = {
            'sampling_event_type': ['exact'],
            'collection': ['exact'],
            'created_on': ['gt', 'lt'],
            'started_on': ['gt', 'lt'],
            'ended_on': ['gt', 'lt']
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
    'sampling_event_type__name',
    'collection_site__site__name',
    'collection__name',
)


ordering_fields = (
    ('created_on', _('created on')),
    ('started_on', _('started on')),
    ('ended_on', _('ended on')),
)
