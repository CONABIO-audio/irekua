from database.models import PhysicalDevice
from .utils import BaseFilter


class PhysicalDeviceFilter(BaseFilter):
    class Meta:
        model = PhysicalDevice
        fields = (
            'device__brand__name',
            'device__model',
            'device__device_type__name',
            'owner__username',
            'owner__first_name'
        )
