from django.utils.translation import gettext as _
from django_filters import FilterSet

from database.models import Site


class Filter(FilterSet):
    class Meta:
        model = Site
        fields = {
            'name': ['exact', 'contains'],
            'locality': ['exact', 'contains'],
            'latitude': ['gt', 'lt'],
            'longitude': ['gt', 'lt'],
            'altitude': ['gt', 'lt'],
            'created_on': ['gt', 'lt'],
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
