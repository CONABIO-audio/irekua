from database.models import DeviceType
from .utils import BaseFilter


search_fields = (
    'name',
)


class Filter(BaseFilter):
    class Meta:
        model = DeviceType
        fields = ('name', )
