from django.utils.translation import gettext as _
from django_filters import FilterSet

from database.models import Licence


class Filter(FilterSet):
    class Meta:
        model = Licence
        fields = {
            'created_on': ['gt', 'lt'],
            'created_by__username': ['exact', 'contains'],
            'licence_type': ['exact'],
        }


search_fields = (
    'internal_id',
    'created_on',
    'created_by',
    'licence_type'
)


ordering_fields = (
    ('created_on', _('added on')),
    ('licence_type', _('licence type')),
)