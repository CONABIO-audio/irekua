from django.utils.translation import gettext as _
from django_filters import FilterSet

from database.models import Collection


class Filter(FilterSet):
    class Meta:
        model = Collection
        fields = [
            'created_on',
            'collection_type',
            'name',
            'institution__institution_name',
            'institution__institution_code',
            'institution__country',
            'is_open',
        ]

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
