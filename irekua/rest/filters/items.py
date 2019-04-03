import django_filters

from database.models import Item
from .utils import BaseFilter


class ItemFilter(BaseFilter):
    is_uploaded = django_filters.BooleanFilter(
        field_name='item_file',
        method='is_uploaded_filter',
        label='is uploaded')

    def is_uploaded_filter(self, queryset, name, value):
        return queryset.filter(item_file__isnull=False)

    class Meta:
        model = Item
        fields = (
            'is_uploaded',
            'item_type__name',
            'sampling_event__sampling_event_type__name',
            'sampling_event__collection__name',
            'sampling_event__collection__collection_type',
            'sampling_event__site__site_type__name',
            'sampling_event__physical_device__device__device_type__name',
            'sampling_event__physical_device__device__brand__name',
        )
