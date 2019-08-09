from django import forms
from django.utils.translation import gettext as _
from django_filters import FilterSet,DateFilter

from database.models import CollectionDevice


class Filter(FilterSet):
    created_on_from = DateFilter(field_name="created_on",lookup_expr='gt',widget=forms.DateInput(attrs={'class': 'datepicker'}))
    created_on_to = DateFilter(field_name="created_on",lookup_expr='lt',widget=forms.DateInput(attrs={'class': 'datepicker'}))    
    class Meta:
        model = CollectionDevice
        fields = {
            'created_by__username': ['contains'],
            'created_by__first_name': ['contains'],
            'created_by__last_name': ['contains'],
            'physical_device__device__brand__name': ['exact', 'contains'],
            'physical_device__device__model': ['exact', 'contains'],
            'physical_device__device__device_type': ['exact']
        }


search_fields = (
    'internal_id',
    'physical_device__serial_number',
    'physical_device__device__brand__name',
    'physical_device__device__model'
)


ordering_fields = (
    ('created_on', _('added on')),
    ('internal_id', _('internal id'))
)
