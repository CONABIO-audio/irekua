from django.utils.translation import gettext as _
from django_filters import FilterSet

from database.models import SamplingEventDevice



class Filter(FilterSet):
    class Meta:
        model = SamplingEventDevice
        fields = [
            'created_on',
            'collection_device__physical_device__device__brand__name',
            'collection_device__physical_device__device__model',
            'collection_device__physical_device__device__device_type',
        ]


search_fields = (
    'collection_device__physical_device__device__serial_number',
    'collection_device__physical_device__device__brand__name',
    'collection_device__physical_device__device__model'
)


ordering_fields = (
    ('created_on', _('added on')),
)

