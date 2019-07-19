from django.utils.translation import gettext as _
from django_filters import FilterSet

from database.models import CollectionSite


class Filter(FilterSet):
    class Meta:
        model = CollectionSite
        fields = {
        'created_on': ['gt', 'lt'],
        'created_by__username': ['exact', 'contains'],
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
