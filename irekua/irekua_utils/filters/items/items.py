from django import forms
from django.utils.translation import gettext as _
from django_filters import FilterSet,DateFilter

from database.models import Item


class Filter(FilterSet):
    created_on_from = DateFilter(field_name="created_on",lookup_expr='gt',widget=forms.DateInput(attrs={'class': 'datepicker'}))
    created_on_to = DateFilter(field_name="created_on",lookup_expr='lt',widget=forms.DateInput(attrs={'class': 'datepicker'}))    
    
    class Meta:
        model = Item
        fields = {
            'created_by__username': ['contains'],
            'created_by__first_name': ['contains'],
            'created_by__last_name': ['contains'],
            'created_by__institution__institution_name': ['contains'],
            'created_by__institution__institution_code': ['exact'],
            'created_by__institution__country': ['contains'],
            'item_type': ['exact'],
            }


search_fields = (
    'item_type__name',
    'created_by__username',
    'created_by__first_name',
    'created_by__last_name',
)


ordering_fields = (
    ('captured_on', _('captured on')),
    ('created_on', _('added on')),
    ('filesize', _('filesize'))
)
