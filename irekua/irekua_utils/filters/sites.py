from django import forms
from django.utils.translation import gettext as _
from django_filters import FilterSet,DateFilter

from database.models import Site


class Filter(FilterSet):
    created_on = DateFilter(widget=forms.DateInput(attrs={'class': 'datepicker'}))    

    class Meta:
        model = Site

        fields = {
            'name': ['exact', 'contains'],
            'locality': ['exact', 'contains'],
            'latitude': ['gt', 'lt'],
            'longitude': ['gt', 'lt'],
            'altitude': ['gt', 'lt'],
        }

search_fields = (
    'name',
    'locality',
)


ordering_fields = (
    ('created_on', _('created on')),
    ('name', _('name')),
    ('locality', _('locality')),
)
