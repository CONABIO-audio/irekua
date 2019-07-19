from django import forms
from django.utils.translation import gettext as _
from django_filters import FilterSet,DateFilter

from database.models import SamplingEvent


class Filter(FilterSet):
    created_on = DateFilter(widget=forms.DateInput(attrs={'class': 'datepicker'}))    
    class Meta:
        model = SamplingEvent
        fields = {
            'sampling_event_type': ['exact'],
            'collection': ['exact'],
            'started_on': ['gt', 'lt'],
            'ended_on': ['gt', 'lt'],
            'created_on': ['gt', 'lt'],
        }

search_fields = (
    'sampling_event_type',
    'collection',
)


ordering_fields = (
    ('created_on', _('created on')),
    ('started_on', _('started on')),
    ('ended_on', _('ended on')),
)
