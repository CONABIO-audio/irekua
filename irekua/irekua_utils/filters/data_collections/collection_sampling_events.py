from django import forms
from django.utils.translation import gettext as _
from django_filters import FilterSet,DateFilter


from database.models import SamplingEvent


class Filter(FilterSet):
    created_on = DateFilter(widget=forms.DateInput(attrs={'class': 'datepicker'}))    
    class Meta:
        model = SamplingEvent
        fields = {
            'created_on': ['gt', 'lt'],
            'created_by__username': ['exact', 'contains'],
            'sampling_event_type': ['exact'],
            'collection_site__site__name': ['exact','contains'],
            'started_on': ['gt', 'lt'],
            'ended_on': ['gt', 'lt'],
        }


search_fields = (
    'internal_id',
    'created_on',
    'created_by',
    'sampling_event_type',
    'collection_site__site__name',
    'started_on',
    'ended_on'
)


ordering_fields = (
    ('created_on', _('added on')),
    ('started_on', _('started on')),
    ('ended_on', _('ended on'))
)