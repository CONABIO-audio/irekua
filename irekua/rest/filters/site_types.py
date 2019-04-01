from database.models import SiteType
from .utils import BaseFilter


class SiteTypeFilter(BaseFilter):
    class Meta:
        model = SiteType
        fields = ('name', )
