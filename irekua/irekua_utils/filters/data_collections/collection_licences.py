from django import forms
from django.db import models
from django.utils.translation import gettext as _
from django_filters import FilterSet,DateFilter

from database.models import Licence


class Filter(FilterSet):
    class Meta:
        model = Licence
        fields = {
            'created_by__username': ['icontains'],
            'created_by__first_name': ['icontains'],
            'created_by__last_name': ['icontains'],
            'licence_type': ['exact'],
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
    'internal_id',
    'created_on',
    'created_by',
    'licence_type'
)


ordering_fields = (
    ('created_on', _('added on')),
    ('licence_type', _('licence type')),
)