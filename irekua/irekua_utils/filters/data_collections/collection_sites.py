from django import forms
from django.utils.translation import gettext as _
from django_filters import FilterSet,DateFilter

from database.models import CollectionSite


class Filter(FilterSet):
    created_on_from = DateFilter(field_name="created_on",lookup_expr='gt',widget=forms.DateInput(attrs={'class': 'datepicker'}))
    created_on_to = DateFilter(field_name="created_on",lookup_expr='lt',widget=forms.DateInput(attrs={'class': 'datepicker'}))    
    class Meta:
        model = CollectionSite
        fields = {
        'created_by__username': ['contains'],
        'created_by__first_name': ['contains'],
        'created_by__last_name': ['contains'],
        'site_type': ['exact'],
        'site__latitude': ['gt', 'lt'],
        'site__longitude': ['gt', 'lt'],
        'site__name': ['exact','contains'],
        'site__locality': ['exact','contains'],
        }


search_fields = (
    'internal_id',
    'site__name',
    'site__locality',
    'site_type__name',
)

ordering_fields = (
    ('created_on', _('added on')),
    ('internal_id', _('internal id'))
)
