from django.utils.translation import gettext as _
from django_filters import FilterSet

from database.models import Licence


class Filter(FilterSet):
    class Meta:
        model = Licence
        fields = [
            'created_on',
            'created_by',
            'licence_type',
            'collection__name',
        ]


search_fields = (
    'internal_id',
    'created_on',
    'created_by',
    'licence_type',
    'collection__name',
)


ordering_fields = (
    ('created_on', _('added on')),
    ('licence_type', _('licence type')),
    ('internal_id', _('internal id'))
)