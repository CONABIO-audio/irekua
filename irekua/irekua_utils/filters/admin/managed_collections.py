from django.utils.translation import gettext as _
from django_filters import FilterSet

from database.models import Collection


class Filter(FilterSet):
    class Meta:
        model = Collection
        fields = {
            'collection_type': ['exact'],
            'institution': ['exact'],
            'created_on': ['gt', 'lt'],
            'is_open': ['exact'],
        }


search_fields = (
    'name',
    'collection_type__name',
    'institution__institution_name'
)

ordering_fields = (
    ('created_on', _('created on')),
)
