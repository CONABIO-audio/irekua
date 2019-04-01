from database.models import SamplingEventType
from .utils import BaseFilter


class SamplingEventTypeFilter(BaseFilter):
    class Meta:
        model = SamplingEventType
        fields = (
            'name',
            'restrict_device_types',
            'restrict_site_types',
        )
