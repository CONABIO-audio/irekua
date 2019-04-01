from database.models import DeviceType
from .utils import BaseFilter


class DeviceTypeFilter(BaseFilter):
    class Meta:
        model = DeviceType
        fields = ('name', )
