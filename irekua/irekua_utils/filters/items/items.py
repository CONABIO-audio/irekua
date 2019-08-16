from django import forms
from django.db import models
from django.utils.translation import gettext as _
from django_filters import FilterSet,DateFilter

from database.models import Item


class Filter(FilterSet):

    class Meta:
        model = Item
        fields = {
            'created_by': ['exact'],
            'created_by__username': ['icontains'],
            'created_by__first_name': ['icontains'],
            'created_by__last_name': ['icontains'],
            'created_by__institution__institution_name': ['icontains'],
            'created_by__institution__institution_code': ['exact'],
            'created_by__institution__country': ['icontains'],
            'item_type': ['exact'],
            'created_on': ['gt', 'lt'],
            }

        filter_overrides = {
            models.DateTimeField: {
                'filter_class': DateFilter,
                'extra': lambda f: {
                    'widget': forms.DateInput(attrs={'class': 'datepicker'})
                }
            }
        }

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
