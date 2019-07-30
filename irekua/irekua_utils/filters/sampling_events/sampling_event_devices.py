from django import forms
from django.utils.translation import gettext as _
from django_filters import FilterSet,DateFilter

from database.models import SamplingEventDevice



class Filter(FilterSet):
    created_on = DateFilter(widget=forms.DateInput(attrs={'class': 'datepicker'}))    

    class Meta:
        model = SamplingEventDevice
        fields = {
            'created_by__username': ['exact', 'contains'],
            'collection_device__physical_device__device__brand__name': ['exact', 'contains'],
            'collection_device__physical_device__device__model': ['exact', 'contains'],
            'collection_device__physical_device__device__device_type': ['exact'],
        }


search_fields = (
    'collection_device__physical_device__device__serial_number',
    'collection_device__physical_device__device__brand__name',
    'collection_device__physical_device__device__model'
)


ordering_fields = (
    ('created_on', _('added on')),
)

