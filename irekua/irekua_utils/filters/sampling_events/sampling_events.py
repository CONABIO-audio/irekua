from django import forms
from django.utils.translation import gettext as _
from django_filters import FilterSet,DateFilter

from database.models import SamplingEvent


class Filter(FilterSet):
    created_on_from = DateFilter(field_name="created_on",lookup_expr='gt',widget=forms.DateInput(attrs={'class': 'datepicker'}))
    created_on_to = DateFilter(field_name="created_on",lookup_expr='lt',widget=forms.DateInput(attrs={'class': 'datepicker'}))    
    ended_on_from = DateFilter(field_name="ended_on",lookup_expr='gt',widget=forms.DateInput(attrs={'class': 'datepicker'}))
    ended_on_to = DateFilter(field_name="ended_on",lookup_expr='lt',widget=forms.DateInput(attrs={'class': 'datepicker'}))
    started_on_from = DateFilter(field_name="started_on",lookup_expr='gt',widget=forms.DateInput(attrs={'class': 'datepicker'}))
    started_on_to = DateFilter(field_name="started_on",lookup_expr='lt',widget=forms.DateInput(attrs={'class': 'datepicker'}))

    class Meta:
        model = SamplingEvent
        fields = {
            'sampling_event_type': ['exact'],
            'collection': ['exact']
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
