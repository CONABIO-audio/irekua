from django import forms
from django.utils.translation import gettext as _
from django_filters import FilterSet,DateFilter

from database.models import CollectionSite


class Filter(FilterSet):
    class Meta:
        model = CollectionSite
        fields = {
            'created_by': ['exact'],
            'created_by__username': ['icontains'],
            'created_by__first_name': ['icontains'],
            'created_by__last_name': ['icontains'],
            'site_type': ['exact'],
            'site__altitude': ['gt', 'lt'],
            'site__latitude': ['gt', 'lt'],
            'site__longitude': ['gt', 'lt'],
            'site__name': ['icontains'],
            'site__locality': ['icontains'],
            'created_on': ['gt', 'lt']
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
