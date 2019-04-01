from database.models import DeviceBrand
from .utils import BaseFilter


class DeviceBrandFilter(BaseFilter):
    class Meta:
        model = DeviceBrand
        fields = ('name', )
