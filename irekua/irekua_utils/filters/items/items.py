from django.utils.translation import gettext as _
from django_filters import FilterSet

from database.models import Item


class Filter(FilterSet):
    class Meta:
        model = Item
        fields = [
            'created_on',
            'created_by__username',
            'created_by__first_name',
            'created_by__last_name',
            'created_by__institution__institution_name',
            'created_by__institution__institution_code',
            'created_by__institution__country',
            'item_type',
        ]


search_fields = (
    'item_type__name',
    'created_by__username',
    'created_by__first_name',
    'created_by__last_name',
)


ordering_fields = (
    ('captured_on', _('captured on')),
    ('created_on', _('added on')),
    ('filesize', _('filesize'))
)
