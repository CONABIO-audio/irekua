from database.models import Device
from .utils import BaseFilter


class DeviceFilter(BaseFilter):
    class Meta:
        model = Device
        fields = (
            'brand__name',
            'model',
            'device_type__name',
        )
