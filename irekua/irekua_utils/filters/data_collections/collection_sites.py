from django.utils.translation import gettext as _
from django_filters import FilterSet

from database.models import CollectionSite


class Filter(FilterSet):
    class Meta:
        model = CollectionSite
        fields = [
            'created_on',
            'created_by',
            'site_type',
            'site__latitude',
            'site__longitude',
            'site__name',
            'site__locality'
        ]


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
