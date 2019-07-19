from django import forms
from django.utils.translation import gettext as _
from django_filters import FilterSet,DateFilter

from database.models import PhysicalDevice


class Filter(FilterSet):
    created_on = DateFilter(widget=forms.DateInput(attrs={'class': 'datepicker'}))    
    class Meta:
        model = PhysicalDevice
        fields = {
            'serial_number': ['exact', 'contains'],
            'device__brand__name': ['exact', 'contains'],
            'device__model': ['exact', 'contains'],
            'bundle': ['exact'],
            'identifier': ['exact', 'contains'],
        }



search_fields = (
    'device__brand__name',
    'device__model',
    'identifier',
)


ordering_fields = (
    ('created_on', _('created on')),
    ('serial_number', _('serial number')),
    ('identifier', _('custom id')),
    ('device__brand__name', _('brand')),
    ('device__model', _('model')),
)
