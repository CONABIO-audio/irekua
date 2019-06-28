from django.utils.translation import gettext as _
from django_filters import FilterSet

from database.models import PhysicalDevice


class Filter(FilterSet):
    class Meta:
        model = PhysicalDevice
        fields = {
            'serial_number': ['exact', 'contains'],
            'device__brand__name': ['exact', 'contains'],
            'device__model': ['exact', 'contains'],
            'bundle': ['exact'],
            'created_on': ['gt', 'lt'],
            'identifier': ['exact', 'contains'],
        }

search_fields = (
    'device__brand__name',
    'device__model',
    'identifier',
)


ordering_fields = (
    ('created_on', _('created on')),
    ('serial_number', _('serial number')),
)
