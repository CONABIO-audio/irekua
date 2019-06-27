from django.utils.translation import gettext as _
from django_filters import FilterSet

from database.models import CollectionDevice


class Filter(FilterSet):
    class Meta:
        model = CollectionDevice
        fields = [
            'created_on',
            'created_by',
            'physical_device__device__brand',
            'physical_device__device__model',
            'physical_device__device__device_type',
        ]


search_fields = (
    'internal_id',
    'physical_device__serial_number',
    'physical_device__device__brand__name',
    'physical_device__device__model'
)


ordering_fields = (
    ('created_on', _('added on')),
    ('internal_id', _('internal id'))
)
