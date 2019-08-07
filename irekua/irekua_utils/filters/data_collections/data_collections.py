from django import forms
from django.utils.translation import gettext as _
from django_filters import FilterSet, DateFilter

from database.models import Collection


class Filter(FilterSet):
    created_on = DateFilter(widget=forms.DateInput(attrs={'class': 'datepicker'}))    
    class Meta:
        model = Collection
        fields = {
            'collection_type': ['exact'],
            'name': ['exact', 'contains'],
            'institution__institution_name': ['exact', 'contains'],
            'institution__institution_code': ['exact'],
            'institution__country': ['exact', 'contains'],
            'is_open': ['exact'],
        }


search_fields = (
    'name',
    'collection_type__name',
    'institution__institution_name',
    'institution__institution_code'
)


ordering_fields = (
    ('created_on', _('created on')),
    ('name', _('name'))
)
